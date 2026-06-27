from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import (
    get_current_user,
    hash_password,
    verify_password,
    verify_recaptcha,
)
from app.models.user import User
from app.models.verification_token import VerificationToken
from app.schemas.user import (
    ChangePassword,
    RefreshRequest,
    RefreshResponse,
    RegisterResponse,
    ResendOtp,
    Token,
    UserLogin,
    UserOut,
    UserRegister,
    UserUpdate,
    VerifyEmail,
)
from app.services.audit_service import get_client_info, log_activity
from app.services.login_rate_limit import (
    check_login_rate_limit,
    record_login_attempt,
)
from app.services.otp_service import create_and_send_otp, resend_otp, verify_otp
from app.services.token_service import (
    create_tokens,
    refresh_access_token,
    revoke_all_user_tokens,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterResponse)
def register(data: UserRegister, request: Request, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        phone=data.phone,
        role="customer",
        is_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    ip, ua = get_client_info(request)
    log_activity(db, user, "Register", module="Auth", description="Account registered", ip_address=ip, user_agent=ua)

    create_and_send_otp(db, user)

    return RegisterResponse(
        message="Registration successful. Please check your email for the OTP code.",
        email=user.email,
    )


@router.post("/verify-email")
def verify_email_endpoint(data: VerifyEmail, request: Request, db: Session = Depends(get_db)):
    user = verify_otp(db, email=data.email, otp_code=data.otp_code)
    ip, ua = get_client_info(request)
    log_activity(db, user, "Verify Email", module="Auth", description="Email verified via OTP", ip_address=ip, user_agent=ua)
    return {"message": "Email verified successfully. You can now log in."}


@router.post("/resend-otp")
def resend_otp_endpoint(data: ResendOtp, db: Session = Depends(get_db)):
    resend_otp(db, email=data.email)
    return {"message": "A new OTP has been sent to your email."}


@router.post("/login", response_model=Token)
async def login(data: UserLogin, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else None

    check_login_rate_limit(db, data.email)

    if data.g_recaptcha_response:
        valid = await verify_recaptcha(data.g_recaptcha_response)
        if not valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification failed. Please try again.",
            )

    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        record_login_attempt(db, data.email, success=False, ip_address=client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        record_login_attempt(db, data.email, success=False, ip_address=client_ip)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    if user.role == "customer" and not user.is_verified:
        record_login_attempt(db, data.email, success=False, ip_address=client_ip)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your email for the OTP code.",
        )

    user.last_login = datetime.now(timezone.utc)
    db.commit()

    record_login_attempt(db, data.email, success=True, ip_address=client_ip)

    ip, ua = get_client_info(request)
    log_activity(db, user, "Login", module="Auth", description="Login successful", ip_address=ip, user_agent=ua)

    tokens = create_tokens(db, user.id)
    return Token(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        user=UserOut.model_validate(user),
    )


@router.post("/refresh", response_model=RefreshResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    tokens = refresh_access_token(db, data.refresh_token)
    return RefreshResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
    )


@router.post("/logout")
def logout(
    data: RefreshRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    revoke_all_user_tokens(db, current_user.id)
    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Logout", module="Auth", description="User logged out", ip_address=ip, user_agent=ua)
    return {"message": "Logged out successfully."}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserOut)
def update_profile(
    data: UserUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    changed = [k for k, v in data.model_dump(exclude_unset=True).items() if v is not None]
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)

    if changed:
        ip, ua = get_client_info(request)
        log_activity(db, current_user, "Update Profile", module="Auth", description=f"Updated: {', '.join(changed)}", ip_address=ip, user_agent=ua)

    return current_user


@router.put("/change-password")
def change_password(
    data: ChangePassword,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    current_user.hashed_password = hash_password(data.new_password)
    db.commit()

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Change Password", module="Auth", description="Password changed", ip_address=ip, user_agent=ua)

    return {"message": "Password changed successfully."}

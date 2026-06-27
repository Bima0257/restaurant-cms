import random
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.models.verification_token import VerificationToken
from app.services.email_service import send_otp_email


def generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"


def create_and_send_otp(db: Session, user: User) -> None:
    otp_code = generate_otp()
    expires_at = datetime.now() + timedelta(
        minutes=settings.OTP_EXPIRE_MINUTES
    )

    token = VerificationToken(
        user_id=user.id,
        otp_code=otp_code,
        expires_at=expires_at,
    )
    db.add(token)
    db.commit()

    send_otp_email(to_email=user.email, otp_code=otp_code, full_name=user.full_name)


def verify_otp(db: Session, email: str, otp_code: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    token = (
        db.query(VerificationToken)
        .filter(
            VerificationToken.user_id == user.id,
            VerificationToken.is_used == False,
        )
        .order_by(VerificationToken.created_at.desc())
        .first()
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No OTP found. Please request a new OTP.",
        )

    if token.attempts >= settings.OTP_MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Too many failed attempts. Please request a new OTP.",
        )

    if token.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new OTP.",
        )

    if token.otp_code != otp_code:
        token.attempts += 1
        db.commit()
        remaining = settings.OTP_MAX_ATTEMPTS - token.attempts
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid OTP. {remaining} attempt(s) remaining.",
        )

    token.is_used = True
    user.is_verified = True
    db.commit()

    return user


def resend_otp(db: Session, email: str) -> None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified.",
        )

    last_token = (
        db.query(VerificationToken)
        .filter(
            VerificationToken.user_id == user.id,
            VerificationToken.is_used == False,
        )
        .order_by(VerificationToken.created_at.desc())
        .first()
    )

    if last_token:
        elapsed = (datetime.now() - last_token.created_at).total_seconds()
        if elapsed < settings.OTP_RESEND_COOLDOWN_SECONDS:
            wait = int(settings.OTP_RESEND_COOLDOWN_SECONDS - elapsed)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Please wait {wait} second(s) before requesting a new OTP.",
            )

        last_token.is_used = True
        db.commit()

    create_and_send_otp(db, user)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.services.password_policy import validate_password


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    role: str = "customer"

    @field_validator("password")
    @classmethod
    def password_meets_policy(cls, v: str, info) -> str:
        email = info.data.get("email", "")
        err = validate_password(v, email=email)
        if err:
            raise ValueError(err)
        return v


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_meets_policy(cls, v: str, info) -> str:
        email = info.data.get("email", "")
        err = validate_password(v, email=email)
        if err:
            raise ValueError(err)
        return v


class UserLogin(BaseModel):
    email: str
    password: str
    g_recaptcha_response: str = ""


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def new_password_meets_policy(cls, v: str) -> str:
        err = validate_password(v)
        if err:
            raise ValueError(err)
        return v


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class VerifyEmail(BaseModel):
    email: str
    otp_code: str


class ResendOtp(BaseModel):
    email: str


class RegisterResponse(BaseModel):
    message: str
    email: str

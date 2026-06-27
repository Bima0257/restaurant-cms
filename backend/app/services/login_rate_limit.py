from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.models.login_attempt import LoginAttempt


def check_login_rate_limit(db: Session, email: str) -> None:
    since = datetime.now(timezone.utc) - timedelta(
        minutes=settings.LOGIN_LOCKOUT_MINUTES
    )
    failed_count = (
        db.query(LoginAttempt)
        .filter(
            LoginAttempt.email == email,
            LoginAttempt.success == False,
            LoginAttempt.created_at >= since,
        )
        .count()
    )

    if failed_count >= settings.LOGIN_MAX_ATTEMPTS:
        earliest = (
            db.query(LoginAttempt)
            .filter(
                LoginAttempt.email == email,
                LoginAttempt.success == False,
                LoginAttempt.created_at >= since,
            )
            .order_by(LoginAttempt.created_at.asc())
            .first()
        )

        if earliest:
            unlock_at = earliest.created_at.replace(tzinfo=timezone.utc) + timedelta(
                minutes=settings.LOGIN_LOCKOUT_MINUTES
            )
            remaining = int((unlock_at - datetime.now(timezone.utc)).total_seconds())
            if remaining > 0:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Too many login attempts. Please try again in {remaining} seconds.",
                )


def record_login_attempt(
    db: Session, email: str, success: bool, ip_address: str | None = None
) -> None:
    attempt = LoginAttempt(
        email=email, ip_address=ip_address, success=success
    )
    db.add(attempt)
    db.commit()

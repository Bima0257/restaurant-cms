import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.models.refresh_token import RefreshToken


def create_access_token(user_id: int) -> str:
    to_encode = {"sub": user_id}
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def _generate_refresh_token_str() -> str:
    return str(uuid.uuid4())


def create_refresh_token(db: Session, user_id: int) -> str:
    token_str = _generate_refresh_token_str()
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    token = RefreshToken(
        user_id=user_id,
        token=token_str,
        expires_at=expires_at,
    )
    db.add(token)
    db.commit()

    return token_str


def create_tokens(db: Session, user_id: int) -> dict:
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(db, user_id),
    }


def refresh_access_token(db: Session, refresh_token_str: str) -> dict:
    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token_str)
        .first()
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    if token.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
        )

    if token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )

    token.is_revoked = True
    db.commit()

    return create_tokens(db, token.user_id)


def revoke_refresh_token(db: Session, refresh_token_str: str) -> None:
    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token_str)
        .first()
    )
    if token:
        token.is_revoked = True
        db.commit()


def revoke_all_user_tokens(db: Session, user_id: int) -> None:
    tokens = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False,
        )
        .all()
    )
    for t in tokens:
        t.is_revoked = True
    db.commit()


def cleanup_expired_tokens(db: Session) -> int:
    now = datetime.now(timezone.utc)
    deleted = (
        db.query(RefreshToken)
        .filter(RefreshToken.expires_at < now)
        .delete()
    )
    db.commit()
    return deleted

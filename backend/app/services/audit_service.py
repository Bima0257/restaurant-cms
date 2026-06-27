from typing import Optional

from fastapi import Request
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import User


def get_client_info(request: Optional[Request]) -> tuple[Optional[str], Optional[str]]:
    if not request:
        return None, None
    ip = request.client.host if request.client else None
    ua = request.headers.get("User-Agent") if request.headers else None
    return ip, ua


def log_activity(
    db: Session,
    user: User,
    activity: str,
    module: Optional[str] = None,
    description: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    log = AuditLog(
        user_id=user.id,
        email=user.email,
        user_role=user.role,
        activity=activity,
        module=module,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(log)
    db.commit()
    return log

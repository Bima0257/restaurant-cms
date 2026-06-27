from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.dependencies import (
    get_current_user,
    hash_password,
    require_superadmin,
)
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.audit_service import get_client_info, log_activity
from app.services.backup_service import (
    create_backup,
    delete_backup,
    get_backup_dir,
    list_backups,
    restore_backup,
)

router = APIRouter(prefix="/api/superadmin", tags=["Superadmin"])


@router.get("/admins", response_model=list[UserOut])
def list_admins(
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    return (
        db.query(User)
        .filter(User.role == "admin")
        .order_by(User.created_at.desc())
        .all()
    )


@router.post(
    "/admins", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
def create_admin(
    data: UserCreate,
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        phone=data.phone,
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Create Admin", module="User Management", description=f"Created admin: {user.email}", ip_address=ip, user_agent=ua)

    return user


@router.put("/admins/{admin_id}", response_model=UserOut)
def update_admin(
    admin_id: int,
    data: UserUpdate,
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not user:
        raise HTTPException(status_code=404, detail="Admin not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Update Admin", module="User Management", description=f"Updated admin: {user.email}", ip_address=ip, user_agent=ua)

    return user


@router.delete("/admins/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: int,
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not user:
        raise HTTPException(status_code=404, detail="Admin not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Delete Admin", module="User Management", description=f"Deleted admin: {user.email}", ip_address=ip, user_agent=ua)

    db.delete(user)
    db.commit()


@router.get("/staff", response_model=list[UserOut])
def list_staff(
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    return (
        db.query(User)
        .filter(User.role == "staff")
        .order_by(User.created_at.desc())
        .all()
    )


@router.post(
    "/staff", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
def create_staff(
    data: UserCreate,
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        phone=data.phone,
        role="staff",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Create Staff", module="User Management", description=f"Created staff: {user.email}", ip_address=ip, user_agent=ua)

    return user


@router.put("/staff/{staff_id}", response_model=UserOut)
def update_staff(
    staff_id: int,
    data: UserUpdate,
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == staff_id, User.role == "staff").first()
    if not user:
        raise HTTPException(status_code=404, detail="Staff not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Update Staff", module="User Management", description=f"Updated staff: {user.email}", ip_address=ip, user_agent=ua)

    return user


@router.delete("/staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(
    staff_id: int,
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == staff_id, User.role == "staff").first()
    if not user:
        raise HTTPException(status_code=404, detail="Staff not found")

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Delete Staff", module="User Management", description=f"Deleted staff: {user.email}", ip_address=ip, user_agent=ua)

    db.delete(user)
    db.commit()


@router.get("/audit-log")
def get_audit_log(
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(200)
        .all()
    )
    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "email": log.email,
            "user_role": log.user_role,
            "activity": log.activity,
            "module": log.module,
            "description": log.description,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        })
    return result


@router.put("/reset-password/{user_id}")
def reset_password(
    user_id: int,
    new_password: str,
    request: Request,
    current_user: User = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = hash_password(new_password)
    db.commit()

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Reset Password", module="User Management", description=f"Reset password for: {user.email}", ip_address=ip, user_agent=ua)

    return {"message": "Password reset successfully"}


@router.post("/backup")
def backup_database(
    request: Request,
    current_user: User = Depends(require_superadmin),
):
    try:
        filepath = create_backup()
        filename = Path(filepath).name
        ip, ua = get_client_info(request)
        audit_db = SessionLocal()
        try:
            log_activity(audit_db, current_user, "Backup Database", module="Database", description=f"Created backup: {filename}", ip_address=ip, user_agent=ua)
        finally:
            audit_db.close()
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/sql",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/backups")
def list_backup_files(
    current_user: User = Depends(require_superadmin),
):
    return list_backups()


@router.get("/backup/download/{filename}")
def download_backup(
    filename: str,
    current_user: User = Depends(require_superadmin),
):
    backup_dir = get_backup_dir()
    filepath = backup_dir / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Backup file not found")
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="application/sql",
    )


@router.post("/backup/restore")
def restore_database(
    file: UploadFile,
    request: Request,
    current_user: User = Depends(require_superadmin),
):
    if not file.filename or not file.filename.endswith(".sql"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a .sql backup file.",
        )

    backup_dir = get_backup_dir()
    temp_path = backup_dir / f"_restore_{file.filename}"
    content = file.file.read()
    temp_path.write_bytes(content)

    try:
        restore_backup(str(temp_path))
        temp_path.unlink(missing_ok=True)
        ip, ua = get_client_info(request)
        audit_db = SessionLocal()
        try:
            log_activity(
                audit_db,
                current_user,
                "Restore Database",
                module="Database",
                description=f"Restored from: {file.filename}",
                ip_address=ip,
                user_agent=ua,
            )
        finally:
            audit_db.close()
        return {"message": "Database restored successfully."}
    except RuntimeError as e:
        temp_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/backup/{filename}")
def delete_backup_file(
    filename: str,
    current_user: User = Depends(require_superadmin),
):
    delete_backup(filename)
    return {"message": "Backup file deleted."}

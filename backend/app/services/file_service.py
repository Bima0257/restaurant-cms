import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def _get_upload_dir() -> Path:
    path = Path(settings.UPLOAD_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_file(file: UploadFile) -> None:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{ext}' not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid MIME type '{file.content_type}'",
        )

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE_MB} MB",
        )


async def save_upload(file: UploadFile) -> str:
    validate_file(file)

    ext = Path(file.filename or "").suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    upload_dir = _get_upload_dir()
    file_path = upload_dir / unique_name

    content = await file.read()
    file_path.write_bytes(content)

    return f"/uploads/{unique_name}"


def delete_file(file_url: str | None) -> None:
    if not file_url:
        return

    relative_path = file_url.lstrip("/")
    full_path = Path(settings.UPLOAD_DIR) / Path(relative_path).name
    if full_path.exists():
        full_path.unlink()

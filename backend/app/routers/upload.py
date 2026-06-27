from fastapi import APIRouter, Depends, UploadFile, File

from app.dependencies import get_current_user
from app.models.user import User
from app.services.file_service import save_upload

router = APIRouter(prefix="/api/upload", tags=["Upload"])


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    file_url = await save_upload(file)
    return {
        "success": True,
        "message": "File uploaded successfully",
        "data": {"url": file_url},
    }

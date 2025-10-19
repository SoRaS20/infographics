import os
import uuid
from fastapi import UploadFile, HTTPException

from app.core.config import settings

def validate_file(file: UploadFile, asset_type: str):
    if asset_type == "image":
        allowed_types = ["image/jpeg", "image/png"]
        max_size = 5 * 1024 * 1024  # 5MB
    elif asset_type == "data":
        allowed_types = ["text/csv", "application/json"]
        max_size = 1 * 1024 * 1024  # 1MB
    else:
        raise ValueError("Invalid asset type")

    if file.content_type not in allowed_types:
        raise HTTPException(400, detail="Invalid file type")
    file_size = len(file.file.read())
    file.file.seek(0)  # Reset pointer
    if file_size > max_size:
        raise HTTPException(400, detail="File too large")
    return file_size

async def save_file(file: UploadFile, asset_type: str):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    subdir = "images" if asset_type == "image" else "data"
    path = os.path.join(settings.UPLOAD_DIR, subdir, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(await file.read())
    return filename, path
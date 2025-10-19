from fastapi import APIRouter, Depends, UploadFile, File
from typing import List

from app.services.upload import validate_file, save_file
from app.crud.asset import create_asset, get_user_assets
from app.db.session import SessionLocal
from app.schemas.asset import Asset
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/uploads", tags=["uploads"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/image", response_model=Asset)
async def upload_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db = Depends(get_db)):
    size = validate_file(file, "image")
    filename, path = await save_file(file, "image")
    asset = create_asset(db, current_user.id, "image", filename, path, size, file.content_type)
    return asset

@router.post("/data", response_model=Asset)
async def upload_data(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db = Depends(get_db)):
    size = validate_file(file, "data")
    filename, path = await save_file(file, "data")
    asset = create_asset(db, current_user.id, "data", filename, path, size, file.content_type)
    return asset

@router.get("/", response_model=List[Asset])
def list_assets(asset_type: str | None = None, current_user: User = Depends(get_current_user), db = Depends(get_db)):
    return get_user_assets(db, current_user.id, asset_type)
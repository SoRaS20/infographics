from pydantic import BaseModel
from datetime import datetime

class AssetBase(BaseModel):
    filename: str
    path: str
    size: int
    mimetype: str

class Asset(AssetBase):
    id: int
    asset_type: str
    upload_date: datetime

    class Config:
        from_attributes = True
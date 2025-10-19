from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func

from app.db.base import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asset_type = Column(String)  # "image" or "data"
    filename = Column(String)
    path = Column(String)
    size = Column(Integer)
    mimetype = Column(String)
    upload_date = Column(DateTime, default=func.now())
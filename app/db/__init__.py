from .base import Base
from .session import engine, SessionLocal

# Import models to create tables
from app.models.user import User
from app.models.asset import Asset

Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session

from app.models.asset import Asset

def create_asset(db: Session, user_id: int, asset_type: str, filename: str, path: str, size: int, mimetype: str):
    db_asset = Asset(user_id=user_id, asset_type=asset_type, filename=filename, path=path, size=size, mimetype=mimetype)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_asset(db: Session, asset_id: int):
    return db.query(Asset).filter(Asset.id == asset_id).first()

def get_user_assets(db: Session, user_id: int, asset_type: str | None = None):
    query = db.query(Asset).filter(Asset.user_id == user_id)
    if asset_type:
        query = query.filter(Asset.asset_type == asset_type)
    return query.all()
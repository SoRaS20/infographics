# from sqlalchemy.orm import Session

# from app.models.user import User
# from app.core.security import get_password_hash

# def get_user_by_username(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()

# def create_user(db: Session, username: str, password: str):
#     hashed_password = get_password_hash(password)
#     db_user = User(username=username, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

from sqlalchemy.orm import Session

from app.models.user import User

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str):
    from app.core.security import get_password_hash  # Delayed import here
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
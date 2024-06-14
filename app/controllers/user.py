from sqlalchemy.orm import Session
from app.models.user import User
from app.helpers.auth import hash_password
from app.schemas.user import UserCreate, UserUpdate


# Create
def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump(exclude={"password"}))
    db_user.password = hash_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Read
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# Index
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


# Update
def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.password = hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


# Delete
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

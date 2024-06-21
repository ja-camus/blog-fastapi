from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.helpers.auth import hash_password
from app.schemas.user import UserCreate, UserUpdate


# Create
def create_user(db: Session, user: UserCreate):
    role = db.query(Role).filter(Role.name == "contributor").first()
    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role_id=role.id
    )
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

    print(f"User with id {user_id} not found.")
    
    if not db_user:
        return None

    user_data = vars(user)
    
    print(f"Updating user with data: {user_data}")

    for key, value in user_data.items():
        if value is not None:
            print(f"Setting {key} to {value}") 
            setattr(db_user, key, value)

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

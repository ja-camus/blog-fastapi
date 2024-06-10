from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, User
from app.database import get_db
from app.controllers.user import (
    get_users,
    get_user,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter()


@router.post("/users/", response_model=User)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.put("/users/{user_id}", response_model=User)
def update_user_route(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    db_user = update_user(db, user_id=user_id, user=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=bool)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return True

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
from app.helpers.auth import (
    check_password,
    create_access_token,
    get_current_user,
    get_current_user_role,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserManager

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login", response_model=dict)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = UserManager.get_user_by_username(db, form_data.username)
    if not user or not check_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=User)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=User)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    current_user_role: str = Depends(get_current_user_role),
):
    if current_user.id != user_id and current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    current_user_role: str = Depends(get_current_user_role),
):
    if current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.put("/users/{user_id}", response_model=User)
def update_user_route(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    current_user_role: str = Depends(get_current_user_role),
):
    if current_user.id != user_id and current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    db_user = update_user(db, user_id=user_id, user=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=bool)
def delete_user_route(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    current_user_role: str = Depends(get_current_user_role),
):
    if current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    success = delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return True

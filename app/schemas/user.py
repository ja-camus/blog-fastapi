from pydantic import BaseModel, Field, EmailStr, validator
from app.database import get_db
from app.models.user import UserManager


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

    @validator("username")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Username must not be empty")
        return v


class UserCreate(UserBase):
    @validator("email")
    def email_must_be_unique(cls, v, values, **kwargs):
        db = next(get_db())
        existing_user = UserManager.get_user_by_email(db, v)
        db.close()
        if existing_user:
            raise ValueError("Email already regasasasistered")
        return v


class UserUpdate(UserBase):
    username: str = None
    email: EmailStr = None
    password: str = None


class User(UserBase):
    id: int
    email: EmailStr

    class ConfigDict:
        orm_mode = True

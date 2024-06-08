from pydantic import BaseModel, Field, EmailStr, field_validator
from app.database import get_db
from app.models.user import UserManager
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

    @field_validator("username")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Username must not be empty")
        return v


class UserCreate(UserBase):
    @field_validator("email")
    def email_must_be_unique(cls, v, values, **kwargs):
        db = next(get_db())
        existing_user = UserManager.get_user_by_email(db, v)
        db.close()
        if existing_user:
            raise ValueError("Email already registered")
        return v


class UserUpdate(UserBase):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class User(UserBase):
    id: int
    email: EmailStr

    class ConfigDict:
        orm_mode = True

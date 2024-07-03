from pydantic import BaseModel
from typing import Optional
from .user import User


class PublicationBase(BaseModel):
    title: str
    content: str


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(PublicationBase):
    title: Optional[str] = None
    content: Optional[str] = None


class Publication(PublicationBase):
    id: int
    user_id: Optional[int] = None
    user: Optional[User] = None

    class ConfigDict:
        orm_mode = True

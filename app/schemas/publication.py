from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PublicationBase(BaseModel):
    title: str
    content: str

class PublicationCreate(PublicationBase):
    pass

class Publication(PublicationBase):
    id: int
    user_id: int

    class ConfigDict:
        orm_mode = True

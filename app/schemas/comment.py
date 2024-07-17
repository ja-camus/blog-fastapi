from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    user_id: int
    publication_id: int

    class ConfigDict:
        orm_mode = True

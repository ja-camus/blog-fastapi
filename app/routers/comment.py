from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.comment import Comment, CommentCreate, CommentUpdate
from app.controllers.comment import (
    create_comment,
    get_comment,
    update_comment,
    delete_comment,
)
from app.helpers.auth import get_current_user
from app.database import get_db
from app.models.user import User

router = APIRouter()


@router.post("/comments/", response_model=Comment)
def create_comment_route(
    comment: CommentCreate,
    publication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.name not in ["contributor", "admin"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    return create_comment(db, comment, current_user.id, publication_id)


@router.get("/comments/{comment_id}", response_model=Comment)
def read_comment_route(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.put("/comments/{comment_id}", response_model=Comment)
def update_comment_route(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_comment(db, comment_id, comment, current_user.id)


@router.delete("/comments/{comment_id}", response_model=Comment)
def delete_comment_route(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_admin = current_user.role.name == "admin"
    return delete_comment(db, comment_id, current_user.id, is_admin)

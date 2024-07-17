from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


def create_comment(
    db: Session, comment: CommentCreate, user_id: int, publication_id: int
):
    db_comment = Comment(
        **comment.dict(), user_id=user_id, publication_id=publication_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()


def update_comment(db: Session, comment_id: int, comment: CommentUpdate, user_id: int):
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this comment"
        )

    for key, value in comment.dict(exclude_unset=True).items():
        setattr(db_comment, key, value)

    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int, user_id: int, is_admin: bool):
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != user_id and not is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )

    db.delete(db_comment)
    db.commit()
    return db_comment

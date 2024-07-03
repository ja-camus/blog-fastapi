from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Publication
from app.schemas.publication import PublicationCreate, PublicationUpdate


def create_publication(db: Session, publication: PublicationCreate, user_id: int):
    db_publication = Publication(
        title=publication.title, content=publication.content, user_id=user_id
    )
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication


def get_publication(db: Session, publication_id: int):
    return db.query(Publication).filter(Publication.id == publication_id).first()


def update_publication(
    db: Session, publication_id: int, publication: PublicationUpdate, user_id: int
):
    db_publication = get_publication(db, publication_id)
    if not db_publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    if db_publication.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this publication"
        )

    for key, value in publication.dict(exclude_unset=True).items():
        setattr(db_publication, key, value)

    db.commit()
    db.refresh(db_publication)
    return db_publication


def delete_publication(db: Session, publication_id: int, user_id: int, is_admin: bool):
    db_publication = get_publication(db, publication_id)
    if not db_publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    if db_publication.user_id != user_id and not is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this publication"
        )
    if not is_admin:
        raise HTTPException(status_code=403, detail="Permission Denied")

    db.delete(db_publication)
    db.commit()
    return db_publication

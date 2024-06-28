from sqlalchemy.orm import Session
from app.models import Publication as PublicationModel
from app.schemas.publication import PublicationCreate


def create_publication(db: Session, publication: PublicationCreate, user_id: int):
    db_publication = PublicationModel(**publication.dict(), user_id=user_id)
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication


def get_publication(db: Session, publication_id: int):
    return (
        db.query(PublicationModel).filter(PublicationModel.id == publication_id).first()
    )

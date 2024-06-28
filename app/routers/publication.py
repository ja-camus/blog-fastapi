from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.publication import Publication, PublicationCreate
from app.schemas.user import User
from app.controllers.publication import create_publication, get_publication
from app.database import get_db
from app.helpers.auth import get_current_user

router = APIRouter()

@router.post("/publications/", response_model=Publication)
def create_publication_route(
    publication: PublicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_publication(db=db, publication=publication, user_id=current_user.id)

@router.get("/publications/{publication_id}", response_model=Publication)
def get_publication_route(
    publication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_publication = get_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return db_publication
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.publication import Publication, PublicationCreate, PublicationUpdate
from app.schemas.user import User
from app.controllers.publication import (
    create_publication,
    get_publication,
    update_publication,
    delete_publication,
)
from app.database import get_db
from app.helpers.auth import (
    get_current_user,
    require_admin,
)

router = APIRouter()


@router.post("/publications/", response_model=Publication)
def create_publication_route(
    publication: PublicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_publication(db=db, publication=publication, user_id=current_user.id)


@router.get("/publications/{publication_id}", response_model=Publication)
def get_publication_route(
    publication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_publication = get_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return db_publication


@router.put("/publications/{publication_id}", response_model=Publication)
def update_publication_route(
    publication_id: int,
    publication: PublicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_publication(
        db=db,
        publication_id=publication_id,
        publication=publication,
        user_id=current_user.id,
    )


@router.delete(
    "/publications/{publication_id}",
    response_model=Publication,
    dependencies=[Depends(require_admin)],
)
def delete_publication_route(
    publication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_admin = current_user.role.name == "admin" if current_user.role else False
    return delete_publication(
        db=db, publication_id=publication_id, user_id=current_user.id, is_admin=is_admin
    )

# app/routers/role.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.role import RoleCreate, RoleUpdate, Role
from app.schemas.user import User
from app.database import get_db
from app.controllers.role import (
    get_roles,
    get_role,
    create_role,
    update_role,
    delete_role,
)
from app.helpers.auth import get_current_user

router = APIRouter()

@router.post("/roles/", response_model=Role)
def create_role_route(
    role: RoleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_role(db=db, role=role)


@router.get("/roles/{role_id}", response_model=Role)
def read_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_role = get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.get("/roles/", response_model=list[Role])
def read_roles(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    roles = get_roles(db, skip=skip, limit=limit)
    return roles


@router.put("/roles/{role_id}", response_model=Role)
def update_role_route(
    role_id: int,
    role_update: RoleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_role = update_role(db, role_id=role_id, role=role_update)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.delete("/roles/{role_id}", response_model=bool)
def delete_role_route(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    success = delete_role(db, role_id=role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return True

from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


def create_role(db: Session, role: RoleCreate):
    db_role = Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Role).offset(skip).limit(limit).all()


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def update_role(db: Session, role_id: int, role: RoleUpdate):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return None

    role_data = vars(role)
    for key, value in role_data.items():
        if value is not None:
            setattr(db_role, key, value)

    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
        return True
    return False

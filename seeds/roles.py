from sqlalchemy.orm import Session
from app.models.role import Role

def seed_roles(db: Session):
    roles = ["admin", "editor", "viewer", "contributor", "guest"]
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            new_role = Role(name=role_name, description=f"{role_name} role")
            db.add(new_role)
            db.commit()
            db.refresh(new_role)
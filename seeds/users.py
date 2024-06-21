from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.helpers.auth import hash_password


def seed_admin_user(db: Session):
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        return

    admin_email = "camus@admin.com"
    admin_username = "Camus"
    admin_password = "adminpassword"

    existing_admin = db.query(User).filter(User.email == admin_email).first()
    if not existing_admin:
        new_admin = User(
            username=admin_username,
            email=admin_email,
            password=hash_password(admin_password),
            role_id=admin_role.id,
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

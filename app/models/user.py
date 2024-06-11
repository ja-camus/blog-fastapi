from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserManager:
    # cls -> similar to self in instance methods
    @classmethod
    def get_user_by_email(cls, db, email: str):
        print(f"Buscando usuario con email: {email}")  # Agregar depuración
        users = db.query(User).all()  # Obtener todos los usuarios para depuración
        print(f"Usuarios en la base de datos: {users}")  # Agregar depuración
        user = db.query(User).filter(User.email == email).first()
        print(f"Usuario encontrado: {user}")  # Agregar depuración
        return user


    @classmethod
    def get_user_by_username(cls, db, username: str):
        return db.query(User).filter(User.username == username).first()

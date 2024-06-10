import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.controllers.user import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
)
from app.schemas.user import UserCreate, UserUpdate
from app.helpers.auth import check_password


class TestUserController:
    # CreateUser
    def test_create_user(self, db: Session):
        user_data = UserCreate(
            username="test_user", email="test@example.com", password="testpassword"
        )

        created_user = create_user(db, user_data)
        assert created_user.username == user_data.username

    def test_create_user_without_username(self, db: Session):
        with pytest.raises(ValidationError):
            user_data = UserCreate(email="test@example.com", password="testpassword")
            create_user(db, user_data)

    def test_create_user_without_email(self, db: Session):
        with pytest.raises(ValidationError):
            user_data = UserCreate(username="test_user", password="testpassword")
            create_user(db, user_data)

    def test_create_user_without_password(self, db: Session):
        with pytest.raises(ValidationError):
            user_data = UserCreate(username="test_user", email="test@example.com")
            create_user(db, user_data)

    # UpdateUser
    def test_update_user(self, db: Session, user):
        updated_data = UserUpdate(
            username="updated_user",
            email="updated@example.com",
            password="updatedpassword",
        )
        updated_user = update_user(db, user.id, updated_data)

        assert updated_user.username == updated_data.username

    def test_update_user_username(self, db: Session, user):
        updated_data = UserUpdate(username="test_user_updated")
        updated_user = update_user(db, user.id, updated_data)

        assert updated_user.username == updated_data.username

    def test_update_user_email(self, db: Session, user):
        updated_data = UserUpdate(email="test_2@example.com")
        updated_user = update_user(db, user.id, updated_data)

        assert updated_user.email == updated_data.email

    def test_update_user_with_invalid_email(self, db: Session, user):
        with pytest.raises(ValueError):
            updated_data = UserUpdate(
                username="updated_user",
                email="invalidemail",
                password="updatedpassword",
            )
            update_user(db, user.id, updated_data)

    def test_update_user_password(self, db: Session, user):
        updated_data = UserUpdate(password="test_user_updated")
        updated_user = update_user(db, user.id, updated_data)

        assert check_password(updated_data.password, updated_user.password)

    def test_update_user_with_invalid_password(self, db: Session, user):
        with pytest.raises(ValidationError):
            updated_data = UserUpdate(password="123")
            update_user(db, user.id, updated_data)

    # Get
    def test_get_user(self, db: Session, user):
        retrieved_user = get_user(db, user.id)
        assert retrieved_user.username == user.username

    def test_get_nonexistent_user(self, db: Session):
        retrieved_user = get_user(db, 99999)

        assert retrieved_user is None

    def test_get_users(self, db: Session, user):
        create_user(
            db,
            UserCreate(
                username="user2", email="user2@example.com", password="password2"
            ),
        )

        users = get_users(db)
        assert len(users) >= 2

    # Delete
    def test_delete_user(self, db: Session, user):
        deleted = delete_user(db, user.id)
        retrieved_user = get_user(db, user.id)

        assert deleted is True
        assert retrieved_user is None

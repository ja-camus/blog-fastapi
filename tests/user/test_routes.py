import pytest
from fastapi import HTTPException
from app.helpers.auth import (
    create_access_token,
    decode_access_token,
)


class TestUserRoutes:
    # CreateUser
    def test_create_user(self, client):
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = client.post("/users/", json=user_data)
        created_user = response.json()

        assert response.status_code == 200
        assert created_user["username"] == user_data["username"]

    def test_create_user_without_username(self, client):
        user_data = {"email": "test@example.com", "password": "testpassword"}
        response = client.post("/users/", json=user_data)

        assert response.status_code == 422

    def test_create_user_without_email(self, client):
        user_data = {"username": "test_user", "password": "testpassword"}
        response = client.post("/users/", json=user_data)

        assert response.status_code == 422

    def test_create_user_without_password(self, client):
        user_data = {"username": "test_user", "email": "test@example.com"}
        response = client.post("/users/", json=user_data)

        assert response.status_code == 422

    # UpdateUser
    def test_update_user_with_invalid_email(self, client, user):
        token = create_access_token(data={"sub": user.email})
        new_data = {"email": "test_updated.com"}
        response = client.put(
            f"/users/{user.id}",
            json=new_data,
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 422

    def test_update_user_with_invalid_password(self, client, user):
        token = create_access_token(data={"sub": user.email})
        new_data = {"password": "123"}
        response = client.put(
            f"/users/{user.id}",
            json=new_data,
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 422

    # GetUser
    def test_get_user(self, client, user):
        token = create_access_token(data={"sub": user.email})
        response = client.get(
            f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
        )
        created_user = response.json()

        assert response.status_code == 200
        assert created_user["email"] == user.email

    def test_get_nonexistent_user(self, client, user):
        token = create_access_token(data={"sub": user.email})
        response = client.get(
            "/users/999999", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403

    def test_get_all_users_as_admin(self, client, db, admin_user):
        token = create_access_token(data={"sub": admin_user.email})
        response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200

    def test_get_all_users_as_non_admin(self, client, user):
        token = create_access_token(data={"sub": user.email})
        response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 403  # No se permite acceder como usuario normal

    # DeleteUser
    def test_delete_user_as_admin(self, client, db, admin_user):
        token = create_access_token(data={"sub": admin_user.email})
        response = client.delete(
            f"/users/{admin_user.id}", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200

    def test_delete_user_as_non_admin(self, client, user):
        token = create_access_token(data={"sub": user.email})
        response = client.delete(
            f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403  # No se permite eliminar como usuario normal

    # Verify decoding of a valid token with an existing user.
    def test_decode_access_token_valid(self, client, db, user):
        token = create_access_token(data={"sub": user.email})
        decoded_user = decode_access_token(db, token)
        assert decoded_user.email == user.email

    # Verify handling of a valid token but with a non-existent user.
    def test_decode_access_token_invalid_user(self, db):
        token = create_access_token(data={"sub": "unexistent_user@email.com"})

        with pytest.raises(HTTPException) as excinfo:
            decode_access_token(token)

        assert excinfo.value.status_code == 401

    # Verify handling of an invalid token (decoding failure).
    def test_decode_access_token_invalid_token(self, db):
        invalid_token = "invalid.token"

        with pytest.raises(HTTPException) as excinfo:
            decode_access_token(invalid_token)

        assert excinfo.value.status_code == 401

    # Verify handling of a token without the "sub" field.
    def test_decode_access_token_missing_sub(self, client, user):
        token = create_access_token(data={})

        with pytest.raises(HTTPException) as excinfo:
            decode_access_token(token)

        assert excinfo.value.status_code == 401

    def test_valid_login(self, client, user):
        login_data = {"username": user.username, "password": "testpassword"}

        response = client.post("/login", data=login_data)

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_invalid_login(self, client, user):
        login_data = {"username": "username_incorrect", "password": "password"}

        response = client.post("/login", data=login_data)

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

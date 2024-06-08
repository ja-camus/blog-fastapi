import pytest


class TestUserRoutes:
    def test_create_user_valid_data(self, client):
        user_data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "newpassword",
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["username"] == user_data["username"]

    # Prueba para manejar la creación de un usuario con datos inválidos
    def test_create_user_invalid_data(self, client):
        user_data = {"email": "new_user@example.com", "password": "newpassword"}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422  # Validación fallida

    def test_get_nonexistent_user(self, client):
        response = client.get("/users/999999")
        assert response.status_code == 404  # No encontrado

    # Prueba para actualizar un usuario
    def test_update_user(self, client):
        user_data = {"username": "test_user", "password": "testpassword"}
        new_data = {"email": "test_updated@example.com"}
        headers = '' # authenticate_user(client)
        response = client.put("/users/", headers=headers, json=new_data)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["email"] == new_data["email"]

    # Prueba para eliminar un usuario
    def test_delete_user(self, client):
        headers = '' # authenticate_user(client)
        response = client.delete("/users/", headers=headers)
        assert response.status_code == 204  # Sin contenido

    # Prueba para obtener todos los usuarios (revisando la autenticación)
    def test_get_all_users(self, client):
        response = client.get("/users/")
        assert response.status_code == 401  # No autorizado

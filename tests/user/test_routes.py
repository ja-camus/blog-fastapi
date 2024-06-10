from app.helpers.utils import check_password


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
    def test_update_user(self, client, user):
        new_data = {"email": "test_updated@example.com"}
        response = client.put(f"/users/{user.id}", json=new_data)
        updated_user = response.json()

        assert response.status_code == 200
        assert updated_user["email"] == new_data["email"]

    def test_update_user_username(self, client, user):
        new_data = {"username": "username_updated"}
        response = client.put(f"/users/{user.id}", json=new_data)
        updated_user = response.json()

        assert response.status_code == 200
        assert updated_user["username"] == new_data["username"]

    def test_update_user_email(self, client, user):
        new_data = {"email": "test_updated@example.com"}
        response = client.put(f"/users/{user.id}", json=new_data)
        updated_user = response.json()

        assert response.status_code == 200
        assert updated_user["email"] == new_data["email"]

    def test_update_user_with_invalid_email(self, client, user):
        new_data = {"email": "test_updated.com"}
        response = client.put(f"/users/{user.id}", json=new_data)

        assert response.status_code == 422

    def test_update_user_password(self, client, user):
        new_data = {"password": "passwordupdated"}
        response = client.put(f"/users/{user.id}", json=new_data)
        updated_user = response.json()

        assert response.status_code == 200
        assert check_password(new_data["password"], updated_user["password"])

    def test_update_user_with_invalid_password(self, client, user):
        new_data = {"password": "123"}
        response = client.put(f"/users/{user.id}", json=new_data)

        assert response.status_code == 422

    # GetUser
    def test_get_user(self, client, user):
        response = client.get(f"/users/{user.id}")
        created_user = response.json()

        assert response.status_code == 200
        assert created_user["email"] == user.email

    def test_get_nonexistent_user(self, client):
        response = client.get("/users/999999")

        assert response.status_code == 404

    def test_get_all_users(self, client):
        response = client.get("/users/")

        assert response.status_code == 200

    # DeleteUser
    def test_delete_user(self, client, user):
        response = client.delete(f"/users/{user.id}")

        assert response.status_code == 200

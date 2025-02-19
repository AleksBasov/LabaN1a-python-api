from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Тест на повторную регистрацию с тем же username/email
def test_duplicate_registration():
    response = client.post(
        "/register/",
        json={"username": "testuser5", "email": "testuser@example.com",
              "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 400


# Тест аутентификации
def test_login():
    response = client.post(
        "/token",
        data={"username": "testuser5", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

# Тест аутентификации с неверным паролем
def test_login_invalid_password():
    response = client.post(
        "/token",
        data={"username": "testuser5", "password": "wrongpassword"},
    )
    assert response.status_code == 401 


# Тест получения списка пользователей
def test_get_users():
    login_response = client.post(
        "/token",
        data={"username": "testuser5", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

# Тест получения информации о текущем пользователе
def test_get_current_user():
    login_response = client.post(
        "/token",
        data={"username": "testuser5", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data

# Тест удаления пользователя
# def test_delete_user():
#     login_response = client.post(
#         "/token",
#         data={"username": "testuser5", "password": "password123"},
#     )
#     access_token = login_response.json()["access_token"]

#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = client.delete("/users/32", headers=headers)
#     assert response.status_code == 200
#     response = client.delete("/users/32", headers=headers)
#     assert response.status_code == 404

# Тест обновления пользователя
def test_update_user():
    login_response = client.post(
        "/token",
        data={"username": "testuser5", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(
        "/users/70",
        headers=headers,
        json={"full_name": "newemail@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "newemail@example.com"







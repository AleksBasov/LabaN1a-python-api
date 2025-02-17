from fastapi.testclient import TestClient
from main import app
import requests
from fastapi import FastAPI, HTTPException
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer
client = TestClient(app)
import time

def test_performance():
    start_time = time.time()
    for _ in range(1000):  
        response = client.get("/users/")
    end_time = time.time()
    
    assert end_time - start_time < 8  

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 401

def test_create_user():
    response = client.post(
    "/register/",
    json={"username": "testuser4", "email": "testuser4@example.com",
    "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser4"
    assert data["email"] == "testuser4@example.com"

def test_successful_authentication():
    url = "http://localhost:8000/token"

   
    data = {"grant_type": "password","username": "testuser","password": "password123"}

    
    response = requests.post(url, data=data)


    if response.status_code == 200:
        print("Успешная аутентификация:", response.json())
    else:
        print("Ошибка аутентификации:", response.status_code, response.text)


def test_incorrect_username_password():
    url = "http://localhost:8000/token"

    
    data2 = {"grant_type": "password","username222": "testuser","password": "password123222"}

    response = requests.post(url, data=data2)


    if response.status_code == 401:
        print("Неверный пароль")

def test_expired_token():
    response = client.post(
        "/token/",
        json={"username": "testuser", "password": "password123"},
    )
    
    token = response.json()["access_token"]
    
    response = client.get(
        "/refresh/",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 403  
    data = response.json()
    assert data["detail"] == "Token has expired"

def test_get_current_user(client, auth_token):
    response = client.get("/users/me", headers=auth_token)
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "current_user"  #
    assert "email" in data  

def test_update_user(client, update_auth_token):
    update_data = {
        "full_name": "New Full Name",
        "email": "new_email@example.com"
    }
    
    response = client.put("/users/me", json=update_data, headers=update_auth_token)
    assert response.status_code == 200
    
    updated_data = response.json()
    assert updated_data["full_name"] == "New Full Name"
    assert updated_data["email"] == "new_email@example.com"

def test_update_user_invalid_data(client, update_auth_token):
    invalid_update_data = {
        "email": "invalid_email",  
    }
    
    response = client.put("/users/me", json=invalid_update_data, headers=update_auth_token)
    assert response.status_code == 422  

def test_update_user_without_token(client):
    update_data = {
        "full_name": "Another Name"
    }
    
    response = client.put("/users/me", json=update_data)
    assert response.status_code == 401  

def test_delete_user(client, auth_token):
    create_response = client.post("/users", json={"full_name": "Test User", "email": "test_user@example.com"}, headers=auth_token)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}", headers=auth_token)
    assert delete_response.status_code == 204

    delete_again_response = client.delete(f"/users/{user_id}", headers=auth_token)
    assert delete_again_response.status_code == 404  

def test_cors_with_allowed_origin(client):
    response = client.options("/users", headers={"Origin": "https://allowed-domain.com"})
    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert response.headers["Access-Control-Allow-Origin"] == "https://allowed-domain.com"

def test_cors_with_disallowed_origin(client):
    response = client.options("/users", headers={"Origin": "https://disallowed-domain.com"})
    assert response.status_code == 403  # Предполагается, что такой источник не разрешен

def test_secure_data_without_token():
    response = client.get("/secure-data/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}

def test_secure_data_with_invalid_token():
    response = client.get("/secure-data/", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}


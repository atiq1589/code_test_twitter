from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_registration():
    response = client.post(
        "/v1/register",
        json={"name": "Md. Atiqul Islam", "username": "atiqul", "password": "123456"},
    )
    assert response.status_code == 201

def test_user_list():
    client.post(
        "/v1/register",
        json={"name": "Md. Atiqul Islam", "username": "atiqul", "password": "123456"},
    )
    response = client.get("/v1/users")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_login():
    client.post(
        "/v1/register",
        json={"name": "Md. Atiqul Islam", "username": "atiqul", "password": "123456"},
    )
    response = client.post(
        "/v1/token",
        data={"username": "atiqul", "password": "123456"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

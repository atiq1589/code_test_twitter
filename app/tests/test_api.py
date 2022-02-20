from fastapi.testclient import TestClient
from app.authentication import IN_MEMORY_DB
from app.db import Database
from main import app

client = TestClient(app)

IN_MEMORY_DB = Database()


def test_registration():
    response = client.post(
        "/v1/register",
        json={"name": "Md. Atiqul Islam", "username": "atiqul3", "password": "123456"},
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
        json={"name": "Md. Atiqul Islam", "username": "atiqul3", "password": "123456"},
    )
    response = client.post(
        "/v1/token",
        data={"username": "atiqul3", "password": "123456"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

def test_follow_failed_without_login():
    response = client.post(
        "/v1/follow?follow_user_id=2"
    )
    assert response.status_code == 401

def test_follow():
    token = client.post(
        "/v1/token",
        data={"username": "atiqul", "password": "string"},
    ).json()

    response = client.post(
        "/v1/follow?follow_user_id=2",
        headers=dict(Authorization=f"{token['token_type']} {token['access_token']}")
    )
    assert response.status_code == 201

def test_tweet():
    token = client.post(
        "/v1/token",
        data={"username": "atiqul", "password": "string"},
    ).json()

    response = client.post(
        "/v1/tweet",
        headers=dict(Authorization=f"{token['token_type']} {token['access_token']}"),
        json=dict(body="This is my first tweet")
    )
    assert response.status_code == 201


def test_feed():
    IN_MEMORY_DB.reset()

    token = client.post(
        "/v1/token",
        data={"username": "atiqul", "password": "string"},
    ).json()

    client.post(
        "/v1/tweet",
        headers=dict(Authorization=f"{token['token_type']} {token['access_token']}"),
        json=dict(body="This is my first tweet")
    )

    client.post(
        "/v1/tweet",
        headers=dict(Authorization=f"{token['token_type']} {token['access_token']}"),
        json=dict(body="This is my second tweet")
    )
    
    response = client.get(
        "/v1/feed",
        headers=dict(Authorization=f"{token['token_type']} {token['access_token']}"),
    )
    response_body = [tweet["body"] for tweet in response.json()]
    assert response.status_code == 200
    assert response_body == ["This is my second tweet", "This is my first tweet"]

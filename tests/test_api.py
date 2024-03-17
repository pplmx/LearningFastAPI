import random

from . import client
from .base import _create_user


def test_livez():
    response = client.get("/livez")
    assert response.status_code == 200


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200


def test_create_user():
    _create_user()


def test_get_users():
    response = client.get("/api/users/")
    assert response.status_code == 200


def test_get_user_id():
    usr = _create_user()
    response = client.get(f"/api/users/{usr.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": usr.id,
        "name": usr.name,
        "email": usr.email,
        "password": usr.password,
    }


def test_update_user():
    usr = _create_user()
    response = client.put(
        f"/api/users/{usr.id}",
        json={
            "name": "test_update_user" + str(random.randint(1, 100000)),
            "email": "test_update_user" + str(random.randint(1, 100000)) + "@x.io",
            "password": "update_secret" + str(random.randint(1, 100000)),
        },
    )
    assert response.status_code == 200
    assert response.json()["id"] == usr.id
    assert response.json()["name"].startswith("test_update_user")
    assert response.json()["email"].startswith("test_update_user")
    assert response.json()["password"].startswith("update_secret")

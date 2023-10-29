import random

from model.user import User

from . import client


def _create_user() -> User:
    response = client.post(
        "/api/users/",
        json={
            "name": "test_create_user" + str(random.randint(1, 100000)),
            "email": "test_create_user" + str(random.randint(1, 100000)) + "@x.io",
            "password": "secret" + str(random.randint(1, 100000)),
        },
    )
    assert response.status_code == 200
    assert response.json()["id"] > 0
    return User(**response.json())

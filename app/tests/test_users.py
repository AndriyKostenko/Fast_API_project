import jwt

from app.security.security import JWT_SECRET_KEY, ALGORITHM
from app.models.schemas import TokenSchema


async def test_create_user(client, db):
    response = await client.post("/sign_up", json={"name": "test_name",
                                                   "surname": "test_surname",
                                                   "age": 21,
                                                   "email": "test@mail.com",
                                                   "password": '12345678',
                                                   "repeated_password": "12345678"})
    assert response.status_code == 201


def test_user_already_exist(client):
    response = client.post("/sign_up", json={"name": "test_name",
                                             "surname": "test_surname",
                                             "age": 21,
                                             "email": "test@mail.com",
                                             "password": '12345678',
                                             "repeated_password": "12345678"})

    assert response.json().get("detail") == "Email already registered!"
    assert response.status_code == 400


async def test_login_user(client):
    response = await client.post("/login", json={"username": "test@mail.com",
                                                 "password": "12345678"})
    tok = TokenSchema(**response.json())

    payload = jwt.decode(
        tok.access_token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
    )
    user_email = payload.get("sub")
    assert user_email == "test@mail.com"
    assert response.status_code == 200


async def test_login_invalid_data(client):
    response = client.post("/login", json={"username": "bob",
                                           "password": "job"})
    assert response.json().get("detail") == "Incorrect email or password"
    assert response.status_code == 403


async def test_list_users_for_unauthorized(client):
    response = await client.get("/users/")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

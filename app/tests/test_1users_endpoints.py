import jwt
import pytest

from app.security.security import JWT_SECRET_KEY, ALGORITHM
from app.models.schemas import TokenSchema


@pytest.mark.asyncio
async def test_create_user(client):
    async with client as cl:
        response = await cl.post("/sign_up", json={"email": "test@mail.com",
                                                   "name": "test_name",
                                                   "surname": "test_surname",
                                                   "age": 21,
                                                   "password": "12345678",
                                                   "repeated_password": "12345678"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_already_exist(client):
    async with client as cl:
        response = await cl.post("/sign_up", json={"email": "test@mail.com",
                                                   "name": "test_name",
                                                   "surname": "test_surname",
                                                   "age": 21,
                                                   "password": "12345678",
                                                   "repeated_password": "12345678"})
    assert response.json().get("detail") == "Email already registered!"
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_user(client):
    async with client as cl:
        response = await cl.post("/login", data={"username": "test@mail.com",
                                                 "password": "12345678"})
        tok = TokenSchema(**response.json())
        payload = jwt.decode(tok.access_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
    assert user_email == "test@mail.com"
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_invalid_data(client):
    async with client as cl:
        response = await cl.post("/login", data={"username": "bob",
                                                 "password": "job"})
    assert response.json().get("detail") == "Incorrect username or password"
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_users_for_unauthorized(client):
    async with client as cl:
        response = await cl.get("/users/")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_get_user(auth_client):
    async with auth_client as cl:
        response = await cl.get('/users/test@mail.com')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_users(auth_client):
    async with auth_client as cl:
        response = await cl.get("/users/")
    assert response.json()[0] == {"email": "test@mail.com",
                                  "name": "test_name",
                                  "surname": "test_surname",
                                  "age": 21,
                                  "last_quiz_done": None,
                                  "last_quiz_score": None,
                                  "last_quiz_done_date": None}
    assert response.status_code == 200




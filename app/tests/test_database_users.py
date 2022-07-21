import pytest

from app.db.crud_user import create_user, delete_user_, get_users
from ..models.schemas import UserSignUp


@pytest.mark.asyncio
async def test_create_user_success(db):
    new_user = {
        "email": "test@mail2.com",
        "name": "test_name",
        "surname": "test_surname",
        "age": 21,
        "password": "12345678",
        "repeated_password": "12345678"}
    create_user_ = await create_user(db=db, user=UserSignUp(**new_user))
    assert create_user_.email == 'test@mail2.com'


@pytest.mark.asyncio
async def test_create_user_not_success(db):
    new_user = {
        "email": "test@mail2.com",
        "name": "test_name",
        "surname": "test_surname",
        "age": 21,
        "password": "12345678",
        "repeated_password": "12345678"}
    create_user_ = await create_user(db=db, user=UserSignUp(**new_user))
    assert create_user_.email == 'boom'


@pytest.mark.asyncio
async def test_all_users_success(db):
    users = await get_users(db=db)
    assert len(users) == 1


@pytest.mark.asyncio
async def test_all_users_not_success(db):
    users = await get_users(db=db)
    assert len(users) == 2


@pytest.mark.asyncio
async def test_delete_user_success(db):
    user_email = "test@mail2.com"
    users = await get_users(db=db)
    new_users = await delete_user_(db=db, user_email=user_email)
    assert len(new_users) == len(users)-1


@pytest.mark.asyncio
async def test_delete_user_not_success(db):
    user_email = "test@mail2.com"
    users = await get_users(db=db)
    new_users = await delete_user_(db=db, user_email=user_email)
    assert len(new_users) != len(users)-1







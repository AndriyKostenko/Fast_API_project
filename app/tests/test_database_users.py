import pytest

from app.db.crud_user import create_user, delete_user_, get_users, get_user_by_email
from ..models.schemas import UserSignUp


@pytest.mark.asyncio
async def test_create_user_success(session):
    new_user = {
        "email": "test@mail.com",
        "name": "test_name",
        "surname": "test_surname",
        "age": 21,
        "password": "12345678",
        "repeated_password": "12345678"}
    create_user_ = await create_user(db=session, user=UserSignUp(**new_user))
    assert create_user_.email == 'test@mail.com'


@pytest.mark.asyncio
async def test_all_users_success(session):
    users = await get_users(db=session)
    assert len(users) == 1


@pytest.mark.asyncio
async def test_get_user_by_email(session):
    res_user = await get_user_by_email(db=session, user_email="test@mail.com")
    assert res_user.email == "test@mail.com"


@pytest.mark.asyncio
async def test_already_req_user(session):
    new_user = {
        "email": "test@mail.com",
        "name": "test_name",
        "surname": "test_surname",
        "age": 21,
        "password": "12345678",
        "repeated_password": "12345678"}
    try:
        create_new_user = await create_user(db=session, user=UserSignUp(**new_user))
    except:
        create_new_user = None
    assert create_new_user is None


@pytest.mark.asyncio
async def test_delete_user(session):
    await delete_user_(db=session, user_email='test@mail.com')
    users = await get_users(db=session)
    assert len(users) == 0

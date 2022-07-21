from typing import List

from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from app.db.crud_user import create_user, get_user_by_email, get_users, delete_user_
from app.db.database import get_db
from app.security.deps import get_current_user
from app.models.schemas import UserSignUp, UserInfo
from app.security.security import create_access_token, create_refresh_token, verify_password


route = APIRouter(tags=['users'])


@route.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@route.post("/sign_up", summary="Create new user")
async def add_user(user: UserSignUp = Depends(UserSignUp), db: Session = Depends(get_db)):
    db_user = await get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    return create_user(db=db, user=user)


@route.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username -> entering your email, not username
    user = await get_user_by_email(db, user_email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@route.get('/me', summary='Get details of currently logged in user', response_model=UserInfo)
async def get_me(user: UserInfo = Depends(get_current_user)):
    return user


@route.get("/users/", summary='Details of all users', response_model=List[UserInfo])
async def all_users(skip: int = 0, limit: int = 100,
                    current_user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if current_user:
        users = await get_users(db, skip=skip, limit=limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return users


@route.get('/users/{user_email}', summary='Get user by email.', response_model=UserInfo)
async def get_user(user_email: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        db_user = await get_user_by_email(db, user_email=user_email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return db_user


@route.delete("/delete_user/{user_email}", summary='Delete user by email.', response_model=List[UserInfo])
async def delete_user(user_email: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        db_user = await get_user_by_email(db, user_email=user_email)
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found.")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"})
    return delete_user_(db=db, user_email=user_email)


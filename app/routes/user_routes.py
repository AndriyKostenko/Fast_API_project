from typing import List
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.crud import create_user, get_user_by_email, delete_user_, get_user_, get_users
from app.database import get_db
from app.models.schemas import UserBase, DeleteUser, get_current_user
from app.security import oauth2_scheme


route = APIRouter(tags=['users'])


@route.get('/')
async def read_users(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@route.get("/users/me")
async def read_users_me(current_user: UserBase = Depends(get_current_user)):
    return current_user


@route.post("/add_user/", response_model=UserBase)
async def add_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    return create_user(db=db, user=user)


#  deleting user but showing an email valid. error.....
@route.delete("/delete_user/", response_model=DeleteUser)
async def delete_user(user: DeleteUser, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found.")
    return delete_user_(db=db, user=user)


@route.get("/users/", response_model=List[UserBase])
async def all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@route.get('/users/{user_id}', response_model=UserBase)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

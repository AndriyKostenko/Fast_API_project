from pydantic import BaseModel, EmailStr, constr
from fastapi import Depends
from app.security import oauth2_scheme


class UserBase(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


def fake_decode_token(token):
    return UserBase()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


class DeleteUser(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class SignInUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SignUpUser(BaseModel):
    name: constr(max_length=50, strip_whitespace=True)
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr, constr, validator


class UserInfo(BaseModel):
    name: constr(max_length=20, strip_whitespace=True)
    surname: constr(max_length=20, strip_whitespace=True)
    age: int

    class Config:
        orm_mode = True


class SystemUser(UserInfo):
    hashed_password: str

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class CreateUser(UserInfo):
    id: int
    email: EmailStr
    hashed_password: str

    # @validator("password", pre=True)
    # def validate_password(cls, hashed_password):
    #     if len(hashed_password) < 8:
    #         raise ValueError('Password must be at least 8 characters in length.')
    #     return hashed_password

    class Config:
        orm_mode = True


class DeleteUser(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class GetUser(BaseModel):
    id: int

    class Config:
        orm_mode = True





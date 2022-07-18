from typing import List

from pydantic import BaseModel, EmailStr, validator
from pydantic.fields import Field
from fastapi import HTTPException, Form


class UserInfo(BaseModel):
    name: str
    surname: str
    age: int
    email: EmailStr

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "User's name": "Andrew",
                "User's surname": "Kostenko",
                "User's age": 28,
                "email": "email@gmail.com"
            }
        }


# bad request
class UserSignUp(BaseModel):
    email: EmailStr
    name: str
    surname: str
    age: int
    password: str = Field(example='password', min_length=8)
    repeated_password: str = Field(example='password')

    @validator('repeated_password')
    def validate_password(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=404, detail="Your passwords don't match")
        return v

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class QuizInfo(BaseModel):
    id: int
    title: str = Field(example='Title')
    description: str = Field(example='Description')
    total_questions: int = Field(example='2')
    quiz_score: int
    owner_email: str = Field(example='Enter here an email of the necessary User\'s email.')

    class Config:
        orm_mode = True


class QuestionInfo(BaseModel):
    id: int
    question: str = Field(example='How many apples on the three?')
    owner_id: int = Field(example='Enter here an id of the necessary Quiz\'s id.')

    class Config:
        orm_mode = True


class AnswerInfo(BaseModel):
    id: int
    answers: str = Field(example='Five')
    correct_answer: str
    owner_id: int = Field(example='Enter here an id of the necessary Question\'s id')

    class Config:
        orm_mode = True


class Question(BaseModel):
    question_1_id: int
    question_2_id: int


class Answer(BaseModel):
    answer_1: str = Form(..., description='(Question will be provided by Front-End.)')
    answer_2: str = Form(..., description='(Question will be provided by Front-End.)')




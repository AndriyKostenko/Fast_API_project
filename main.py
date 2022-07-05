from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


users = [
    {'name':'Andrew',
     'surname':'Kostenko',
     'age':28},
    {'name':'Max',
     'surname': 'Kostenko',
     'age':14}
]


class Users(BaseModel):
    name: str
    surname: str
    age: int


@app.get("/")
async def all_users():
    return {'users': users}


@app.get("/add_user/")
async def add_user(name: str, surname: str, age: int):
    if {'name': name, 'surname': surname, 'age': age} in users:
        print('Such user already exist.')
    else:
        users.append({'name': name, 'surname': surname, 'age': age})
    return {'name': name, 'surname': surname, 'age': age}


@app.get("/delete_user/")
async def delete_user(name: str, surname: str, age: int):
    if {'name': name, 'surname': surname, 'age': age} in users:
        users.remove({'name': name, 'surname': surname, 'age': age})
    else:
        pass
    return {'users': users}
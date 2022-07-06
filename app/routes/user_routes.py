from fastapi import HTTPException
from fastapi import APIRouter
from models.user_models import User


route = APIRouter(tags=['users'])

users = [
    {'name':'Andrew',
     'surname':'Kostenko',
     'age':28},
    {'name':'Max',
     'surname': 'Kostenko',
     'age':14}
]


@route.get("/")
async def all_users():
    return {'users': users}


@route.get('/users/{user_id}')
def get_user(user_id: int):
    try:
        return {'user_info': users[user_id-1]} # to get started from 1
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@route.post("/add_user/")
async def add_user(user: User):
    print(user)
    if user in users:
        raise HTTPException(status_code=409, detail='Such user already exist.')
    else:
        users.append(user)
    return {'users': users}


@route.delete("/delete_user/")
async def delete_user(user: User):
    if user in users:
        users.remove(user)
    else:
        raise HTTPException(status_code=404, detail='User not found.')
    return {'users': users}

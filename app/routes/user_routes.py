from fastapi import HTTPException
from fastapi import APIRouter

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
        return {'user_info': users[user_id]}
    except IndexError:
        raise HTTPException(status_code=404, detail='Not found')


@route.post("/add_user/")
async def add_user(name: str, surname: str, age: int):
    if {'name': name, 'surname': surname, 'age': age} in users:
        print('Such user already exist.')
    else:
        users.append({'name': name, 'surname': surname, 'age': age})
    return {'name': name, 'surname': surname, 'age': age}


@route.get("/delete_user/")
async def delete_user(name: str, surname: str, age: int):
    if {'name': name, 'surname': surname, 'age': age} in users:
        users.remove({'name': name, 'surname': surname, 'age': age})
    else:
        print('Such user isn\'t exist.')
    return {'users': users}

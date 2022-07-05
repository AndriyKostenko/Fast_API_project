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
async def read_root():
    return {'Hello': 'World'}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, 'q':q}

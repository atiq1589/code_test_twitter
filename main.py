from random import random
from fastapi import FastAPI, Response, status
from db import Database
from models.users import User
from typing import List


app = FastAPI()

IN_MEMORY_DB = Database()

@app.get('/')
async def main():
    return {'message': "This is a Simple Twitter Like App"}


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: User, response: Response):
    if IN_MEMORY_DB.find('users', username=user.username):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return dict(message="Username already found. Please choose a different username.")
    else:
        IN_MEMORY_DB.insert('users', user.dict())


@app.get('/users', response_model=List[User])
async def getAllUsers():
    return IN_MEMORY_DB.find('users')

    
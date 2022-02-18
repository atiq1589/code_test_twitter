from app.db import Database
from app.models import User
from app.models.forms import UserRegistrationModel
from app.authentication import get_password_hash, Token, authenticate_user, create_access_token, get_current_user
from fastapi import APIRouter, Response, status, Depends, HTTPException
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

IN_MEMORY_DB = Database()

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user_form: UserRegistrationModel, response: Response):
    if IN_MEMORY_DB.find('users', username=user_form.username):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return dict(message="Username already found. Please choose a different username.")
    else:
        user = User(**user_form.dict())
        user_dict = user.dict()
        user_dict["hashed_password"] = get_password_hash(user_form.password)
        IN_MEMORY_DB.insert('users', user_dict)


@router.get('/users', response_model=List[User])
async def getAllUsers():
    return IN_MEMORY_DB.find('users')


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
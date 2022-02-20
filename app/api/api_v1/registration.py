from app.models import User
from app.models.forms import UserRegistrationModel
from app.authentication import get_password_hash
from fastapi import APIRouter, Body, Response, status, HTTPException
from app.db.mongo import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(response: Response, user_form: UserRegistrationModel = Body(...)):
    db = get_db()
    user = await db.users.find_one( { "username": user_form.username } )
    if not user:
        user = User(**user_form.dict())
        user_dict = jsonable_encoder(user)
        user_dict["hashed_password"] = get_password_hash(user_form.password)
        inserted = await db.users.insert_one(user_dict)
        if inserted:
            return user
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already exists. Please choose a different username.",
        headers={"WWW-Authenticate": "Bearer"},
    )

import asyncio
from pkgutil import get_data
from urllib import response
from app.cache import set_cache, get_cache
from app.db import Database, in_memory
from app.db.mongo import get_db
from app.db.mongo import get_db
from app.models import User, Tweet
from app.models.forms import UserRegistrationModel, TweetModel
from app.authentication import get_password_hash, Token, authenticate_user, create_access_token, get_current_user
from fastapi import APIRouter, Response, status, Depends, HTTPException, BackgroundTasks
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from app.api.api_v1 import registration_router, auth_router


router = APIRouter()

async def set_follow_cache(user_id, follow_user_id, **kwargs):
    db = get_db()
    key = f"{user_id}_USER_FOLLOW"
    users = await get_cache(key)
    if not users:
        users = []
    users.append(follow_user_id)
    await set_cache(key, users, **kwargs)
    db.user_follow.insert_one(dict(user_id=user_id, follow_user_id=follow_user_id))

@router.post('/follow', status_code=status.HTTP_201_CREATED)
async def follow_user(
    follow_user_id: str,
    response: Response, 
    background_tasks: BackgroundTasks, 
    current_user: User = Depends(get_current_user)):
    """
    This api will added user follow
    It will be write back cache approach
    """
    db = get_db()
    result = await db.user_follow.find_one(dict(user_id=current_user.id, follow_user_id=follow_user_id))
    follow_user = await db.users.find_one(dict(_id=follow_user_id))
    if follow_user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User can't follow ownself.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not follow_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not result:
        background_tasks.add_task(set_follow_cache, current_user.id, follow_user_id)
    else:
        response.status_code = status.HTTP_202_ACCEPTED
    return True
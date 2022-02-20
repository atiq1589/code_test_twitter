from app.cache import set_cache, get_cache
from app.db import Database
from app.db.mongo import get_db
from app.models import User, Tweet
from app.authentication import get_current_user
from fastapi import APIRouter, status, Depends, BackgroundTasks
from typing import List
from app.api.api_v1 import registration_router, auth_router, follow_router, tweet_router, feed_router

router = APIRouter()

IN_MEMORY_DB = Database()


@router.get('/users', response_model=List[User])
async def getAllUsers(current_user: User = Depends(get_current_user)):
    db = get_db()
    users = []
    async for user in db.users.find():
        users.append(user)
    return users

router.include_router(registration_router, tags=['user-registration'])
router.include_router(auth_router, tags=['user-authentication'])
router.include_router(follow_router, tags=['social'])
router.include_router(tweet_router, tags=['social'])
router.include_router(feed_router, tags=['social'])

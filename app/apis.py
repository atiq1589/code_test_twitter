import asyncio
from pkgutil import get_data
from app.cache import set_cache, get_cache
from app.db import Database, in_memory
from app.db.mongo import get_db
from app.models import User, Tweet
from app.models.forms import UserRegistrationModel, TweetModel
from app.authentication import get_password_hash, Token, authenticate_user, create_access_token, get_current_user
from fastapi import APIRouter, Response, status, Depends, HTTPException, BackgroundTasks
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from app.api.api_v1 import registration_router, auth_router, follow_router

router = APIRouter()

IN_MEMORY_DB = Database()


@router.get('/users', response_model=List[User])
async def getAllUsers(current_user: User = Depends(get_current_user)):
    db = get_db()
    users = []
    async for user in db.users.find():
        users.append(user)
    return users


@router.post('/tweet', status_code=status.HTTP_201_CREATED)
def create_tweet(tweet: TweetModel, current_user: User = Depends(get_current_user)):
    tweet_model = Tweet(**dict(user_id=current_user.id, body=tweet.body))
    IN_MEMORY_DB.insert('tweets', tweet_model.dict())


@router.get('/feed', status_code=status.HTTP_200_OK, response_model=List[Tweet])
async def create_tweet(background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    follow_key = f"{current_user.id}_USER_FOLLOW"
    feed_key = f"{current_user.id}_USER_FEED"
    feed = await get_cache(feed_key)
    user_follow = []
    if not feed:
        user_follow = await get_cache(follow_key)

    if not user_follow and not feed:
        user_follow = IN_MEMORY_DB.find('user_follow', user_id=current_user.id)
        background_tasks.add_task(set_cache, follow_key, [current_user.id] + [user["follow_user_id"] for user in user_follow])

    if not feed:
        feed = IN_MEMORY_DB.find_in('tweets', user_id=user_follow)
        feed.sort(key=lambda item: item['created_at'], reverse=True)
        background_tasks.add_task(set_cache, feed_key, feed, ex=30)

    return feed

router.include_router(registration_router, tags=['user-registration'])
router.include_router(auth_router, tags=['user-authentication'])
router.include_router(follow_router, tags=['social'])

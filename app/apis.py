import asyncio
from app.cache import set_cache, get_cache
from app.db import Database, in_memory
from app.models import User, Tweet
from app.models.forms import UserRegistrationModel, TweetModel
from app.authentication import get_password_hash, Token, authenticate_user, create_access_token, get_current_user
from fastapi import APIRouter, Response, status, Depends, HTTPException, BackgroundTasks
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from app.api.api_v1 import registration

router = APIRouter()

IN_MEMORY_DB = Database()

async def set_follow_cache(user_id, follow_user_id, **kwargs):
    key = f"{user_id}_USER_FOLLOW"
    users = await get_cache(key)
    if not users:
        users = []
    users.append(follow_user_id)
    await set_cache(key, users, **kwargs)
    IN_MEMORY_DB.insert("user_follow", dict(user_id=user_id, follow_user_id=follow_user_id))


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


@router.post('/follow', status_code=status.HTTP_201_CREATED)
async def follow_user(follow_user_id: int, response: Response, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    result = IN_MEMORY_DB.find('user_follow', user_id=current_user.id, follow_user_id=follow_user_id)
    follow_user = IN_MEMORY_DB.find('users', id=follow_user_id)
    if follow_user_id == current_user.id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return dict(message="User can't follow ownself.")
    if not follow_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return dict(message="Requested User not found.")
    if not result:
        background_tasks.add_task(set_follow_cache, current_user.id, follow_user_id)


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

router.include_router(registration.router, tags=['user-registration'])

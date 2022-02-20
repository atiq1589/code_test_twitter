from app.cache import set_cache, get_cache
from app.db.mongo import get_db
from app.models import User, Tweet
from app.authentication import get_current_user
from fastapi import APIRouter, status, Depends, BackgroundTasks
from typing import List

router = APIRouter()

@router.get('/feed', status_code=status.HTTP_200_OK, response_model=List[Tweet])
async def generate_feed(background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    db = get_db()
    follow_key = f"{current_user.id}_USER_FOLLOW"
    feed_key = f"{current_user.id}_USER_FEED"
    feed = await get_cache(feed_key)
    user_follow = []
    if not feed:
        user_follow = await get_cache(follow_key)
    if not user_follow and not feed:
        user_follow = [current_user.id]
        async for doc in db.user_follow.find(dict(user_id=current_user.id)):
            user_follow.append(doc["follow_user_id"])
        background_tasks.add_task(set_cache, follow_key, user_follow)

    if not feed:
        feed = []
        print(user_follow)
        async for doc in db.tweets.find({"user_id": {"$in": user_follow}}).sort('created_at', -1):
            feed.append(doc)
        background_tasks.add_task(set_cache, feed_key, feed, ex=10)
    return feed

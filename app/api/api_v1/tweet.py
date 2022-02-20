from app.db.mongo import get_db
from app.models import User, Tweet
from app.models.forms import TweetModel
from app.authentication import get_current_user
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post('/tweet', status_code=status.HTTP_201_CREATED)
async def create_tweet(tweet: TweetModel, current_user: User = Depends(get_current_user)):
    """
    This api will create tweets but will not wait for success
    # TODO: in future need to replace with background task
    """
    db = get_db()
    tweet_model = Tweet(**dict(user_id=current_user.id, body=tweet.body))
    db.tweets.insert_one(jsonable_encoder(tweet_model))

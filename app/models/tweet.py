from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr

class Tweet(BaseModel):
    """
    Tweet model 
    Replicate DB record
    """   
    _TWEET_COUNT: int = 0 # will be replaced in future with real db
    id: Optional[int] = None
    user_id: int
    body: constr(min_length=3, max_length=140)
    created_at: datetime = datetime.utcnow()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = Tweet._TWEET_COUNT + 1
            Tweet._TWEET_COUNT += 1

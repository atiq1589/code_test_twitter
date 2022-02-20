from pydantic import BaseModel, constr


class TweetModel(BaseModel):
    """
    Tweet model 
    """   
    body: constr(min_length=3, max_length=140)

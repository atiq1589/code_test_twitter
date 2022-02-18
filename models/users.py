from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """
    User model 
    Replicate DB record
    """   
    _USER_COUNT: int = 0 # will be replaced in future with real db
    id: Optional[int] = None
    name: str
    username: str
    password: str

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = User._USER_COUNT + 1
            User._USER_COUNT += 1


class UserLoginModel(BaseModel):
    """
    User login model
    """
    username: str
    password: str

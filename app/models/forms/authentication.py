from pydantic import BaseModel


class UserRegistrationModel(BaseModel):
    """
    User Registration model 
    Replicate HTML Form
    """   
    name: str
    username: str
    password: str

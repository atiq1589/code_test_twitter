import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, constr

class Tweet(BaseModel):
    """
    Tweet model this model sharded by user_id in DB
    Be careful changing this model
    """   
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    user_id: uuid.UUID # BECAREFUL TO CHANGE THIS FIELD
    body: constr(min_length=3, max_length=140)
    created_at: datetime = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": 'd2c64531-0a66-4efe-b34f-aa5f63d6251e',
                "user_id": '80bb1a41-ccd9-45b2-b949-d2c79584a6d7',
                "body": "my tweet",
                "created_at": "2022-02-20T09:18:44.625024"
            }
        }

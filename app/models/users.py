from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field


class User(BaseModel):
    """
    User model 
    """   
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    username: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": 'd2c64531-0a66-4efe-b34f-aa5f63d6251e',
                "name": "Md. Atiqul Islam",
                "username": "atiqul"
            }
        }

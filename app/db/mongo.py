from collections import defaultdict
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from app.settings import settings

class Mongo:
    """
    This class will provide Mongo connection as singleton instance
    """
    _instance = None
   
    def __init__(self) -> None:
        # TODO: will replace with settings / environment 
        self.client = AsyncIOMotorClient(settings.DB_CONNECTION)

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Mongo, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __exit__(self, type, value, traceback):
        self.client.close()
    


"""
Consumer can directly use from this connection instance
"""
driver = Mongo()
connection = driver.client

def get_db(db_name:str = 'twitterDb'):
    return connection[db_name]

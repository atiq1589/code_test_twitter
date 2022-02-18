"""
This is a super simple in memory DB to prototype an Application
"""

from collections import defaultdict
from typing import Any


class Database:
    """
    This class will provide simple python dictionary
    to store metadata that gives a feel like Database
    """
    _instance = None
   
    def __init__(self) -> None:
        self.tables = defaultdict(list)
        self.tables['users'] = [
            dict(id=1, name="Md. Atiqul Islam", username="atiqul", hashed_password="$2b$12$Uk7ATB/OtBrU7qiM.sLPoeB1MoLz1C3qQddR/5jVlkxPnJ1GKBdHq"),
            dict(id=2, name="Md. Atiqul Islam", username="atiqul2", hashed_password="$2b$12$Uk7ATB/OtBrU7qiM.sLPoeB1MoLz1C3qQddR/5jVlkxPnJ1GKBdHq")
        ]

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def insert(self, table_name: str, model: dict) -> bool:
        """
        This method will allow to insert an entry to a table

        Parameter:
        ----------
        table_name: str
            Table Name 
        model: dict
            Python dictionary that represent an entry
        
        Return:
        -------
        bool
            True if successfully added or False otherwise
        """
        try:
            self.tables[table_name].append(model)
        except Exception:
            return False
        else:
            return True
        
    
    def find(self, table_name: str, **kwargs) -> list:
        """
        This method will find entries form table for given query

        Parameters:
        -----------
        table_name: str
            Table name for run the query
        kwargs: dict
            Any given keyword arguments that will test the table for result
        
        Raises:
        -------
        Exception
            if key not found in the table rows
        
        Return:
        -------
        list
            Will return list of dictionary against the query
        """
        try:
            query = filter(lambda entry: all(entry[key] == value for key,value in kwargs.items()), self.tables[table_name])
            result = list(query)
        except Exception:
            raise Exception("Invalid Query")
        else:
            return result

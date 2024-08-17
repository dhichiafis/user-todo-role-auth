from pydantic import BaseModel 
from typing import List 
from enum import Enum
from datetime import datetime,date
class Role(str,Enum):
    ADMIN='admin'
    TEACHER='teacher'
    STUDENT='student'
    
class ItemBase(BaseModel):
    title:str 
    description:str 

class ItemList(ItemBase):
    owner_id:int 
    id:int 
    #created_at:date
    
    class Config:
        orm_mode=True 
        arbitrary_types_allowed=True 
    
class UserBase(BaseModel):
    username:str 
    password:str 
    role:Role 

class UserList(UserBase):
    items:List[ItemList]=[]
    id:int 
    
    class Config:
        orm_mode=True
        arbitrary_types_allowed=True
        


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


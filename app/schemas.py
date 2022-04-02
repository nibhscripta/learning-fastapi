from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


#response sent when a particular user data is retrieved   
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

        
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True
    owner: UserResponse

    
class PostCreate(PostBase):
    pass


#response sent when a post is retrieved
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
        
    class Config:
        orm_mode = True
        
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
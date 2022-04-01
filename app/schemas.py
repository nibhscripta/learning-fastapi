from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True

    
class PostCreate(PostBase):
    pass


#response sent when a post is retrieved
class PostResponse(PostBase):
    id: int
    created_at: datetime
        
    class Config:
        orm_mode = True
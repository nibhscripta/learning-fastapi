from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2, time
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
    rating: Optional[int] = None 


#these aren't real credentials
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='dev', 
            user='dev', 
            password='dev',
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print('connected to db')
        break
    except Exception as error:
        print(f'Failed to conect to db. The error was: {error}')
        time.sleep(2)


my_posts = [
    {'title': 'the 1st post', 'content': 'the content of the 1st post', 'published': True, 'rating': 0, 'id': 1},
    {'title': 'best frameworks', 'content': 'fastapi obviously', 'published': True, 'rating': 0, 'id': 2}
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
     
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sql")
def test_posts(db: Session = Depends(get_db)):
    return {'message': 'succes on db conn'}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict =post.dict()
    post_dict['id'] = randrange(2, 1000000)
    my_posts.append(post_dict)
    return {'data': post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    return {'data': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'detail': post_dict}
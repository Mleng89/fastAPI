from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    # id: int


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 1000000)
    print("Do I have a rating?", post.rating)
    my_posts.append(post_dict)
    return {"new_post": post}


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"post": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # int_id = int(id)
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found.",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Error": f"Post with id: {id} was not found."}

    return {"data": post}

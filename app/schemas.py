from datetime import datetime
from typing import Optional, List, Annotated
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOnly(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    owner_id: int
    owner: UserOnly


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    Post: Post
    votes: int


# Defined after PostOut, because it uses PostOut
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime
    posts: List[PostOut]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]
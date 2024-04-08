from typing import Any

from pydantic import BaseModel
from pydantic import validator

from peewee import ModelSelect

from pydantic.utils import GetterDict

class PeeweGetterDict(GetterDict):
    def get(self, key:Any, default=None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 5 or len(username) > 50:
            raise ValueError("Username must be at least 3 characters")
        return username
    
# ----------- User ----------------

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweGetterDict


class UserResponseModel(ResponseModel):
    id: int
    username: str

# ----------- Movie ----------------

class MovieResponseModel(ResponseModel):
    id: int
    title: str




# ----------- Review ----------------

class ReviewValidator():

    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError("Score must be between 1 and 5")
        return score
    

class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movie_id: int
    review: str
    score: int


class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel
    review: str
    score: int


class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int


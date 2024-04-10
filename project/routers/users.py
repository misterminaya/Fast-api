from typing import List
from fastapi import Response
from fastapi import Cookie
from fastapi import HTTPException,APIRouter
from fastapi import Depends

from fastapi.security import HTTPBasicCredentials

from ..database import User

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel
from ..schemas import ReviewResponseModel

from ..common import oauth2_scheme
from ..common import get_current_user


router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail="User already exists")

    hashed_password = User.create_password_hash(user.password)

    user = User.create(username=user.username, password=hashed_password)
    return UserResponseModel(id=user.id, username=user.username)


@router.post("/login", response_model=UserResponseModel)
async def login_user(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.password != User.create_password_hash(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    response.set_cookie(key="user_id", value=str(user.id))

    return user


"""
@router.get("/reviews", response_model=List[ReviewResponseModel])
async def get_user_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return [ user_review for user_review in user.reviews]
"""

@router.get("/reviews", response_model=List[ReviewResponseModel])
async def get_user_reviews(user: User = Depends(get_current_user)):
    return [ user_review for user_review in user.reviews]
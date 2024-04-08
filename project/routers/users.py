from fastapi import HTTPException,APIRouter

from ..database import User

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel


router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail="User already exists")

    hashed_password = User.create_password_hash(user.password)

    user = User.create(username=user.username, password=hashed_password)
    return UserResponseModel(id=user.id, username=user.username)
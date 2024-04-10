import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from fastapi import status, HTTPException


from fastapi import Depends
from .database import User

SECRET_KEY = "CodigoMinaya#2021"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")


def create_access_token(user, days=20):
    data = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(seconds=days)
    }

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    data =  decode_access_token(token)

    if data:
        return User.select().where(User.id == data.get('user_id')).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"})
  

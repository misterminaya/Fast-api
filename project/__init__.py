from fastapi import FastAPI
from fastapi import APIRouter

from .database import User, Movie, UserReview
from .routers import users_router
from .routers import reviews_router


from .database import database as connection


app = FastAPI(title="FastAPI App", description="FastAPI App", version="1.0.0")

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(users_router)
api_v1.include_router(reviews_router)


app.include_router(api_v1)

@app.on_event("startup")
def start_app():
    if connection.is_closed():
        connection.connect()
        
    connection.create_tables([User, Movie, UserReview])

@app.on_event("shutdown")
def stop_app():
    if not connection.is_closed():
        connection.close()




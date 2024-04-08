from typing import List
from fastapi import FastAPI
from fastapi import HTTPException

from database import User, Movie, UserReview
from database import database as connection

from schemas import UserRequestModel
from schemas import UserResponseModel
from schemas import ReviewRequestModel
from schemas import ReviewResponseModel
from schemas import ReviewRequestPutModel

app = FastAPI(title="FastAPI App", description="FastAPI App", version="1.0.0")

@app.on_event("startup")
def start_app():
    if connection.is_closed():
        connection.connect()
        
    connection.create_tables([User, Movie, UserReview])

@app.on_event("shutdown")
def stop_app():
    if not connection.is_closed():
        connection.close()
        

@app.get("/")
async def index():
    return {"Hello": "World"}

@app.get("/about")
async def about():
    return {"About": "FastAPI App"}


@app.post("/users", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail="User already exists")

    hashed_password = User.create_password_hash(user.password)

    user = User.create(username=user.username, password=hashed_password)
    return UserResponseModel(id=user.id, username=user.username)


@app.post("/reviews", response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).first() == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if Movie.select().where(Movie.id == user_review.movie_id).first() == None:    
        raise HTTPException(status_code=404, detail="Movie not found")

    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review


@app.get("/reviews", response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)
    return [user_review for user_review in reviews]


@app.get("/reviews/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int):
    review = UserReview.select().where(UserReview.id == review_id).first()
    
    if review == None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@app.put("/reviews/{review_id}", response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    
    if user_review == None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()
    
    return user_review


@app.delete("/reviews/{review_id}", response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    
    if user_review == None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.delete_instance()
    return user_review
from fastapi import FastAPI
from pydantic import BaseModel

from app.services.crewai_service import generate_review

app = FastAPI()


class ReviewRequest(BaseModel):
    winning_movie: str


@app.get("/")
def root():
    return {"message": "Nermie Backend Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/generate-review")
def generate_movie_review(request: ReviewRequest):
    return generate_review(request.winning_movie)

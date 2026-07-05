import requests
from app.config import CREWAI_API_URL, CREWAI_BEARER_TOKEN


def generate_review(winning_movie: str):
    return {
        "status": "ready",
        "movie": winning_movie
    }

import requests
from app.config import CREWAI_API_URL, CREWAI_BEARER_TOKEN


def generate_review(winning_movie: str):

    headers = {
        "Authorization": f"Bearer {CREWAI_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {
            "winning_movie": winning_movie
        },
        "taskWebhookUrl": "",
        "stepWebhookUrl": "",
        "crewWebhookUrl": "",
        "trainingFilename": ""
    }

    response = requests.post(
        f"{CREWAI_API_URL}/kickoff",
        headers=headers,
        json=payload,
        timeout=120
    )

    return response.json()

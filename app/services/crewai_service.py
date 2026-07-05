import time
import requests

from app.config import CREWAI_API_URL, CREWAI_BEARER_TOKEN


headers = {
    "Authorization": f"Bearer {CREWAI_BEARER_TOKEN}",
    "Content-Type": "application/json"
}


def generate_review(winning_movie: str):

    # ---------------------------
    # STEP 1 - Start Crew
    # ---------------------------

    kickoff_url = f"{CREWAI_API_URL}/kickoff"

    payload = {
        "inputs": {
            "winning_movie": winning_movie
        }
    }

    kickoff_response = requests.post(
        kickoff_url,
        headers=headers,
        json=payload
    )

    kickoff_response.raise_for_status()

    kickoff_id = kickoff_response.json()["kickoff_id"]

    # ---------------------------
    # STEP 2 - Wait for completion
    # ---------------------------

    status_url = f"{CREWAI_API_URL}/status/{kickoff_id}"

    while True:

        response = requests.get(
            status_url,
            headers=headers
        )

        response.raise_for_status()

        result = response.json()

        status = result.get("status")

        print(status)

        if status == "COMPLETED":
            return result

        elif status == "FAILED":
            raise Exception("CrewAI execution failed.")

        time.sleep(3)

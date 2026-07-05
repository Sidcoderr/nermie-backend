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
    # STEP 2 - Poll Until Finished
    # ---------------------------

    status_url = f"{CREWAI_API_URL}/status/{kickoff_id}"

    timeout = 300  # 5 minutes
    start = time.time()

    while True:

        response = requests.get(
            status_url,
            headers=headers
        )

        response.raise_for_status()

        result = response.json()

        # If CrewAI has produced the review
        if result.get("result") is not None:
            return {
                "success": True,
                "movie": winning_movie,
                "review": result["result"]
            }

        # Crew failed
        if result.get("state") == "FAILED":
            raise Exception("CrewAI execution failed.")

        # Timeout
        if time.time() - start > timeout:
            raise Exception("CrewAI execution timed out.")

        # Wait before checking again
        time.sleep(3)

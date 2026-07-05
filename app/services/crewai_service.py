import time
import requests

from app.config import CREWAI_API_URL, CREWAI_BEARER_TOKEN

headers = {
    "Authorization": f"Bearer {CREWAI_BEARER_TOKEN}",
    "Content-Type": "application/json"
}


def generate_review(winning_movie: str):

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

    print("Kickoff Status Code:", kickoff_response.status_code)
    print("Kickoff Response:", kickoff_response.text)

    kickoff_response.raise_for_status()

    kickoff_id = kickoff_response.json()["kickoff_id"]

    print("Kickoff ID:", kickoff_id)

    status_url = f"{CREWAI_API_URL}/status/{kickoff_id}"

    print("Status URL:", status_url)

    timeout = 300          # wait up to 5 minutes
    start = time.time()

    while True:

        response = requests.get(
            status_url,
            headers=headers
        )

        print("-----------------------------------")
        print("Status Code:", response.status_code)
        print("Raw Response:")
        print(response.text)

        response.raise_for_status()

        result = response.json()

        state = result.get("state")
        status = result.get("status")

        print("State :", state)
        print("Status:", status)

        # -------- SUCCESS --------

        if result.get("result") is not None:
            print("Result Found")
            return result

        if result.get("result_json") is not None:
            print("Result JSON Found")
            return result

        if result.get("output") is not None:
            print("Output Found")
            return result

        # -------- FAILED --------

        if state == "FAILED":
            raise Exception("CrewAI execution failed.")

        if status and "failed" in status.lower():
            raise Exception("CrewAI execution failed.")

        # -------- TIMEOUT --------

        if time.time() - start > timeout:
            raise Exception("CrewAI execution timed out after 5 minutes.")

        print("Still waiting...")
        time.sleep(3)

import time
import requests

from app.config import CREWAI_API_URL, CREWAI_BEARER_TOKEN

headers = {
    "Authorization": f"Bearer {CREWAI_BEARER_TOKEN}",
    "Content-Type": "application/json"
}


def generate_review(winning_movie: str):

    # ---------------------------
    # STEP 1 - Kickoff Crew
    # ---------------------------

    kickoff_url = f"{CREWAI_API_URL}/kickoff"

    payload = {
        "inputs": {
            "winning_movie": winning_movie
        }
    }

    print("Starting CrewAI...")
    print("Kickoff URL:", kickoff_url)
    print("Payload:", payload)

    kickoff_response = requests.post(
        kickoff_url,
        headers=headers,
        json=payload
    )

    print("Kickoff Status Code:", kickoff_response.status_code)
    print("Kickoff Response:", kickoff_response.text)

    kickoff_response.raise_for_status()

    kickoff_json = kickoff_response.json()

    kickoff_id = kickoff_json.get("kickoff_id")

    if not kickoff_id:
        raise Exception(f"No kickoff_id returned.\nResponse: {kickoff_json}")

    print("Kickoff ID:", kickoff_id)

    # ---------------------------
    # STEP 2 - Poll Status
    # ---------------------------

    status_url = f"{CREWAI_API_URL}/status/{kickoff_id}"

    print("Status URL:", status_url)

    timeout = 180   # 3 minutes
    start = time.time()

    while True:

        if time.time() - start > timeout:
            raise Exception("Timed out waiting for CrewAI.")

        response = requests.get(
            status_url,
            headers=headers
        )

        print("--------------------------------")
        print("Status Code:", response.status_code)
        print("Raw Response:")
        print(response.text)
        print("--------------------------------")

        response.raise_for_status()

        result = response.json()

        # Return immediately if CrewAI already returned final output
        if "result" in result:
            print("Final Result Found")
            return result

        if "output" in result:
            print("Final Output Found")
            return result

        status = (
            result.get("status")
            or result.get("state")
            or result.get("execution_status")
        )

        print("Detected Status:", status)

        if status:

            status = status.upper()

            if status in ["COMPLETED", "SUCCESS", "FINISHED"]:
                return result

            if status in ["FAILED", "ERROR"]:
                raise Exception(f"CrewAI Failed:\n{result}")

        time.sleep(3)

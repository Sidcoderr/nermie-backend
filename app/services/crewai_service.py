import time
import requests

from app.config import CREWAI_API_URL, CREWAI_BEARER_TOKEN


headers = {
    "Authorization": f"Bearer {CREWAI_BEARER_TOKEN}",
    "Content-Type": "application/json"
}


def generate_review(winning_movie: str):

    # -----------------------------------------
    # STEP 1 - Start CrewAI Workflow
    # -----------------------------------------

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

    kickoff_data = kickoff_response.json()

    kickoff_id = kickoff_data["kickoff_id"]

    print(f"CrewAI Execution Started: {kickoff_id}")

    # -----------------------------------------
    # STEP 2 - Poll Until Finished
    # -----------------------------------------

    status_url = f"{CREWAI_API_URL}/status/{kickoff_id}"

    timeout = 300
    start_time = time.time()

    while True:

        response = requests.get(
            status_url,
            headers=headers
        )

        response.raise_for_status()

        result = response.json()

        print(result)

        # Workflow Finished
        if result.get("result") is not None:

            execution_time = round(time.time() - start_time, 2)

            return {
                "success": True,

                "movie": winning_movie,

                "review": result["result"],

                "crew": {
                    "provider": "CrewAI Cloud",

                    "status": "Completed",

                    "execution_id": kickoff_id,

                    "execution_time": execution_time,

                    "workflow": "Movie Review Crew",

                    "agents": [
                        {
                            "name": "Community Analyst",
                            "status": "Completed"
                        },
                        {
                            "name": "Movie Researcher",
                            "status": "Completed"
                        },
                        {
                            "name": "Director Expert",
                            "status": "Completed"
                        },
                        {
                            "name": "Genre Specialist",
                            "status": "Completed"
                        },
                        {
                            "name": "Film Critic",
                            "status": "Completed"
                        },
                        {
                            "name": "Publisher",
                            "status": "Completed"
                        }
                    ]
                }
            }

        # Workflow Failed
        if result.get("state") == "FAILED":

            raise Exception("CrewAI execution failed.")

        # Timeout
        if time.time() - start_time > timeout:

            raise Exception("CrewAI execution timed out.")

        time.sleep(3)

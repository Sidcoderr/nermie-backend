from dotenv import load_dotenv
import os

load_dotenv()

CREWAI_API_URL = os.getenv("CREWAI_API_URL")
CREWAI_BEARER_TOKEN = os.getenv("CREWAI_BEARER_TOKEN")

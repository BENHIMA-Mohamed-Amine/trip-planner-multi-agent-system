import os
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "trip-planner-agent")

AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
os.environ["AMADEUS_HOSTNAME"] = "test"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables.")

if not AMADEUS_CLIENT_ID or not AMADEUS_CLIENT_SECRET:
    raise ValueError("Amadeus API credentials are not set in environment variables.")

if not LANGSMITH_API_KEY:
    raise ValueError("LANGSMITH_API_KEY is not set in environment variables.")

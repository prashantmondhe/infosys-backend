import os
from dotenv import load_dotenv
from google import genai

from backend.config.env_config import GEMINI_API_KEY, GOOGLE_API_KEY

load_dotenv()

api_key = GEMINI_API_KEY or GOOGLE_API_KEY

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key

# ३. Client व Models
client = genai.Client(api_key=api_key, vertexai=False) if api_key else None

GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_MODEL_NAME = "gemini-3.6-flash"

# Using 3072-dimension embedding model to match the existing vector store
GEMINI_EMBEDDING_MODEL = "models/gemini-embedding-2"
EMBEDDING_MODEL = "models/gemini-embedding-2"
EMBEDDING_DIMENSION = 3072

GOOGLE_API_KEY = api_key
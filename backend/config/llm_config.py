from google import genai
from .env_config import envConfig

#  Configuring Gemini

# GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSION = 1536

client = genai.Client(
    api_key=envConfig.GEMINI_API_KEY
    )
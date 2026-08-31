import os
from backend.config.env_config import GEMINI_API_KEY, GOOGLE_API_KEY

# सुरक्षितपणे API Key मिळवणे
api_key = GEMINI_API_KEY or GOOGLE_API_KEY

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key
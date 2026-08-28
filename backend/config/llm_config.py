import os
import streamlit as st
from google import genai

# Read API Key from st.secrets or os.environ
api_key = None
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY", "")

# Initialize GenAI Client
client = genai.Client(api_key=api_key)
GEMINI_MODEL = "gemini-1.5-flash"
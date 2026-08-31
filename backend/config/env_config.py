import os
from dotenv import load_dotenv

load_dotenv()

# Streamlit Cloud वर deploy केलं असेल तरच हे काम करेल, Railway वर हा भाग सायलेंटली स्किप होतो
try:
    import streamlit as st
    try:
        for k, v in st.secrets.items():
            if isinstance(v, str):
                os.environ[k] = v
    except Exception:
        pass
except Exception:
    pass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
GOOGLE_API_KEY = GEMINI_API_KEY
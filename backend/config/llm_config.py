import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
    or ""
)

if not api_key:
    try:
        import streamlit as st
        try:
            api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY") or ""
        except Exception:
            pass
    except Exception:
        pass


if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key

# ३. Client व Models कॉ
client = genai.Client(api_key=api_key) if api_key else None

GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_MODEL_NAME = "gemini-3.6-flash"

# Using 3072-dimension embedding model to match the existing vector store
GEMINI_EMBEDDING_MODEL = "models/gemini-embedding-2"
EMBEDDING_MODEL = "models/gemini-embedding-2"
EMBEDDING_DIMENSION = 3072

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2",
    google_api_key=api_key
)
EMBEDDINGS = embeddings
GOOGLE_API_KEY = api_key
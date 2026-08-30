import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY", "")

try:
    import streamlit as st
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key

client = genai.Client(api_key=api_key)

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

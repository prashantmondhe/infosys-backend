import os
import streamlit as st
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Read API Key
api_key = ""
if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY", "")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key

# Initialize GenAI Client
client = genai.Client(api_key=api_key)

# Model identifiers supported by v1beta
GEMINI_MODEL = "models/gemini-1.5-flash"
GEMINI_MODEL_NAME = "models/gemini-1.5-flash"
GEMINI_EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_DIMENSION = 768

# LangChain Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model=GEMINI_EMBEDDING_MODEL,
    google_api_key=api_key
)
EMBEDDINGS = embeddings
GOOGLE_API_KEY = api_key

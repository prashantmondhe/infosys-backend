import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

try:
    import streamlit as st
    for k, v in st.secrets.items():
        if isinstance(v, str) and k not in os.environ:
            os.environ[k] = v
except Exception:
    pass

class EnvConfig(BaseSettings):
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "sqlite:///backend/infosys_ai.db")
    CHROMA_PERSIST_DIRECTORY: Optional[str] = os.getenv("CHROMA_PERSIST_DIRECTORY", "vector_db")
    JWT_SECRET_KEY: Optional[str] = os.getenv("JWT_SECRET_KEY", "default_secret_key_123")
    ENVIRONMENT: Optional[str] = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        extra = "ignore"

envConfig = EnvConfig()

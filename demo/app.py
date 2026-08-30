import os
import sys
from pathlib import Path
from typing import Optional, List, Any, Dict

# =====================================================
# 1. Environment & Streamlit Secrets Polyfill
# =====================================================
# Ensures RAG pipeline reads Railway env variables without secrets.toml
import streamlit as st

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY", "")
try:
    st.secrets["GOOGLE_API_KEY"] = api_key
    st.secrets["GEMINI_API_KEY"] = api_key
except Exception:
    class SecretsMock(dict):
        def __getattr__(self, key):
            return self.get(key, "")

    st.secrets = SecretsMock({
        "GOOGLE_API_KEY": api_key,
        "GEMINI_API_KEY": api_key,
        "default": {
            "GOOGLE_API_KEY": api_key,
            "GEMINI_API_KEY": api_key
        }
    })

# =====================================================
# 2. Python Path Configuration
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = PROJECT_ROOT / "backend"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# =====================================================
# 3. Third-Party Imports & FastAPI Setup
# =====================================================
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from backend.GenAI.ai_workflows.orchestration.rag_pipeline import (
    RAGPipeline,
)

app = FastAPI(
    title="Enterprise GPT API",
    description="FastAPI backend serving enterprise RAG pipeline and Auth",
    version="1.0.0",
)

# Enable CORS for Next.js frontend (Vercel & Localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory user store for demo authentication
USERS_DB: Dict[str, dict] = {}

# =====================================================
# 4. Initialize RAG Pipeline Instance
# =====================================================
try:
    pipeline = RAGPipeline()
    print("✓ RAG Pipeline initialized successfully.")
except Exception as e:
    print(f"Warning: Initial pipeline load deferred: {e}")
    pipeline = None

# =====================================================
# 5. Request & Response Schemas
# =====================================================
class QueryRequest(BaseModel):
    query: str
    designation: Optional[str] = "HR Operations Lead"

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "Employee"

class LoginRequest(BaseModel):
    email: str
    password: str

# =====================================================
# 6. API Endpoints
# =====================================================
@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "Enterprise GPT Backend is running on Port 8000"
    }

# --- Authentication Endpoints ---
@app.post("/api/register")
@app.post("/register")
async def register_user(payload: RegisterRequest):
    email_clean = payload.email.strip().lower()
    
    if not payload.name or not email_clean or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name, email, and password are required."
        )

    # Save to in-memory store
    USERS_DB[email_clean] = {
        "name": payload.name,
        "email": email_clean,
        "password": payload.password,
        "role": payload.role or "Employee"
    }

    return {
        "status": "success",
        "message": "User registered successfully",
        "user": {
            "name": payload.name,
            "email": email_clean,
            "role": payload.role or "Employee"
        }
    }

@app.post("/api/login")
@app.post("/login")
async def login_user(payload: LoginRequest):
    email_clean = payload.email.strip().lower()
    user = USERS_DB.get(email_clean)

    # Allow login if credentials match or fallback for demo testing
    if user and user["password"] == payload.password:
        return {
            "status": "success",
            "message": "Login successful",
            "user": {
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }
    elif not user:
        # Auto-create/demo login fallback so testing is seamless
        role_guess = "HR Operations Lead" if "hr" in email_clean else "Employee"
        name_guess = email_clean.split("@")[0].capitalize()
        return {
            "status": "success",
            "message": "Login successful",
            "user": {
                "name": name_guess,
                "email": email_clean,
                "role": role_guess
            }
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password."
    )

# --- RAG Query Endpoint ---
@app.post("/api/query")
@app.post("/query")
async def execute_query(payload: QueryRequest):
    global pipeline
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Lazy-load pipeline if initial startup deferred
    if pipeline is None:
        try:
            pipeline = RAGPipeline()
        except Exception as err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize RAG Pipeline: {str(err)}"
            )

    try:
        # Execute enterprise RAG query
        result = pipeline.answer(
            query=payload.query.strip(),
            designation=payload.designation or "HR Operations Lead",
        )

        # Parse citations safely
        citations_data = []
        if hasattr(result, "citations") and result.citations:
            for c in result.citations:
                citations_data.append({
                    "citation_id": getattr(c, "citation_id", None),
                    "document_name": getattr(c, "document_name", None),
                    "document_id": getattr(c, "document_id", None),
                    "chunk_id": getattr(c, "chunk_id", None),
                    "page_number": getattr(c, "page_number", None),
                })

        return {
            "status": "success",
            "answer": result.answer if hasattr(result, "answer") else str(result),
            "citations": citations_data,
            "metadata": getattr(result, "metadata", {})
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline execution error: {str(exc)}"
        )


if __name__ == "__main__":
    uvicorn.run("demo.app:app", host="0.0.0.0", port=8000, reload=True)
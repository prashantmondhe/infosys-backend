import os
import sys
from pathlib import Path
from typing import Optional, List, Any

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
    # Fallback dictionary mapping if st.secrets is immutable
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
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from backend.GenAI.ai_workflows.orchestration.rag_pipeline import (
    RAGPipeline,
)

app = FastAPI(
    title="Enterprise GPT API",
    description="FastAPI backend serving enterprise RAG pipeline",
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

# =====================================================
# 6. API Endpoints
# =====================================================
@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "Enterprise GPT Backend is running on Port 8000"
    }

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
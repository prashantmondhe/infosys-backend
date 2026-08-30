import os
import sys
from pathlib import Path
from typing import Optional, List, Any, Dict

# =====================================================
# 1. Automatic Streamlit Secrets.toml File Generator
# =====================================================
# Railway वर /app/.streamlit/secrets.toml आणि ~/.streamlit/secrets.toml आपोआप तयार करणे
api_key = (
    os.getenv("GOOGLE_API_KEY")
    or os.getenv("GEMINI_API_KEY")
    or os.getenv("OPENAI_API_KEY")
    or ""
)

secrets_content = f"""
GOOGLE_API_KEY = "{api_key}"
GEMINI_API_KEY = "{api_key}"

[default]
GOOGLE_API_KEY = "{api_key}"
GEMINI_API_KEY = "{api_key}"
"""

# सर्व संभाव्य Linux पाथ्सवर secrets.toml तयार करणे
possible_secret_dirs = [
    Path.cwd() / ".streamlit",
    Path("/app/.streamlit"),
    Path("/root/.streamlit"),
    Path.home() / ".streamlit",
]

for s_dir in possible_secret_dirs:
    try:
        s_dir.mkdir(parents=True, exist_ok=True)
        s_file = s_dir / "secrets.toml"
        s_file.write_text(secrets_content.strip(), encoding="utf-8")
        print(f"✓ Created secrets.toml at: {s_file}")
    except Exception as e:
        pass

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

# Streamlit secrets mock (In-memory fallback)
import streamlit as st
try:
    st.secrets["GOOGLE_API_KEY"] = api_key
    st.secrets["GEMINI_API_KEY"] = api_key
except Exception:
    pass

app = FastAPI(
    title="Enterprise GPT API",
    description="FastAPI backend serving enterprise RAG pipeline",
    version="1.0.0",
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy Pipeline variable
pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        from backend.GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
        pipeline = RAGPipeline()
    return pipeline

# =====================================================
# 4. Request Schemas
# =====================================================
class QueryRequest(BaseModel):
    query: str
    designation: Optional[str] = "HR Operations Lead"

# =====================================================
# 5. API Endpoints
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
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        rag = get_pipeline()
        result = rag.answer(
            query=payload.query.strip(),
            designation=payload.designation or "HR Operations Lead",
        )

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
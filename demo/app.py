import os
import sys
from pathlib import Path

# =====================================================
# 1. Force Physical secrets.toml Creation on Linux Disk
# =====================================================
api_key = (
    os.getenv("GOOGLE_API_KEY")
    or os.getenv("GEMINI_API_KEY")
    or os.getenv("OPENAI_API_KEY")
    or ""
)

secrets_body = f"""GOOGLE_API_KEY = "{api_key}"
GEMINI_API_KEY = "{api_key}"

[default]
GOOGLE_API_KEY = "{api_key}"
GEMINI_API_KEY = "{api_key}"
"""

for target_dir in [
    Path("/root/.streamlit"),
    Path("/app/.streamlit"),
    Path.home() / ".streamlit",
    Path.cwd() / ".streamlit"
]:
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "secrets.toml").write_text(secrets_body.strip(), encoding="utf-8")
    except Exception:
        pass

# Streamlit in-memory mock
try:
    import streamlit as st
    st.secrets["GOOGLE_API_KEY"] = api_key
    st.secrets["GEMINI_API_KEY"] = api_key
except Exception:
    pass

# =====================================================
# 2. Path Setup
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = PROJECT_ROOT / "backend"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# =====================================================
# 3. FastAPI Initialization & RAG Pipeline
# =====================================================
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Enterprise GPT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        from backend.GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
        pipeline = RAGPipeline()
    return pipeline

class QueryRequest(BaseModel):
    query: str
    designation: str = "HR Operations Lead"

@app.get("/")
def health():
    return {"status": "ok", "message": "Enterprise GPT Backend is active"}

@app.post("/api/query")
@app.post("/query")
async def execute_query(payload: QueryRequest):
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        rag = get_pipeline()
        result = rag.answer(
            query=payload.query.strip(),
            designation=payload.designation,
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
        raise HTTPException(status_code=500, detail=f"Failed to load RAG Pipeline: {str(exc)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
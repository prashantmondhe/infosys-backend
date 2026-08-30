import sys
from pathlib import Path
from typing import Optional, List, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# =====================================================
# Python paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = PROJECT_ROOT / "backend"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# =====================================================
# RAG Pipeline Import
# =====================================================

from backend.GenAI.ai_workflows.orchestration.rag_pipeline import (
    RAGPipeline,
)

# =====================================================
# Initialize FastAPI App & CORS
# =====================================================

app = FastAPI(
    title="Enterprise GPT API",
    description="FastAPI backend providing RAG Pipeline query capabilities",
    version="1.0.0"
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
# Initialize RAG Pipeline Instance
# =====================================================

try:
    pipeline = RAGPipeline()
except Exception as e:
    print(f"Warning: RAG Pipeline initialization deferred or failed: {e}")
    pipeline = None

# =====================================================
# Request / Response Schemas
# =====================================================

class QueryRequest(BaseModel):
    query: str
    designation: Optional[str] = "HR Operations Lead"

# =====================================================
# API Endpoints
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

    if pipeline is None:
        try:
            pipeline = RAGPipeline()
        except Exception as err:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to load RAG Pipeline: {str(err)}"
            )

    try:
        # Execute enterprise RAG pipeline
        result = pipeline.answer(
            query=payload.query.strip(),
            designation=payload.designation or "HR Operations Lead",
        )

        # Format citations
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
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
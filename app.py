import os
import sys
from pathlib import Path
from typing import Optional, Any, Dict

# =====================================================================
# १. Path Setup
# =====================================================================
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

for p in [CURRENT_DIR, PROJECT_ROOT, BACKEND_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# =====================================================================
# २. Environment Variables (आता फक्त env_config.py वरून)
# =====================================================================
from backend.config.env_config import GEMINI_API_KEY, GOOGLE_API_KEY

api_key = GOOGLE_API_KEY or GEMINI_API_KEY

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key

# =====================================================================
# ३. Google Generative AI
# =====================================================================
try:
    import google.generativeai as genai
    if api_key:
        genai.configure(api_key=api_key)
except Exception:
    pass

# =====================================================================
# ४. RAG Pipeline
# =====================================================================
pipeline_instance = None

def get_rag_pipeline():
    global pipeline_instance
    if pipeline_instance is not None:
        return pipeline_instance

    try:
        from GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
        pipeline_instance = RAGPipeline()
        return pipeline_instance
    except Exception:
        pass

    try:
        from backend.GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
        pipeline_instance = RAGPipeline()
        return pipeline_instance
    except Exception as e:
        raise RuntimeError(f"Failed to load RAG Pipeline: {str(e)}")

# =====================================================================
# ५. FastAPI Setup
# =====================================================================
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Enterprise GPT API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    designation: Optional[str] = "HR Operations Lead"

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Enterprise GPT Backend is active"}

@app.post("/api/query")
@app.post("/query")
async def handle_query(payload: QueryRequest):
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        rag = get_rag_pipeline()

        try:
            result = rag.answer(payload.query.strip(), designation=payload.designation)
        except TypeError:
            result = rag.answer(payload.query.strip(), payload.designation)

        if isinstance(result, dict):
            final_answer = (
                result.get("answer")
                or result.get("response")
                or result.get("output")
                or str(result)
            )
            citations = result.get("citations", [])
        elif hasattr(result, "answer"):
            final_answer = result.answer
            citations = getattr(result, "citations", [])
        elif hasattr(result, "content"):
            final_answer = result.content
            citations = []
        else:
            final_answer = str(result)
            citations = []

        return {
            "status": "success",
            "answer": final_answer,
            "citations": citations
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(exc)}")

# =====================================================================
# ६. Run
# =====================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
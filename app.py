import os
import sys
from pathlib import Path
from typing import Optional, Any, Dict

# =====================================================================
#
# =====================================================================
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

for p in [CURRENT_DIR, PROJECT_ROOT, BACKEND_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# =====================================================================
# २. Environment Variables 
# =====================================================================
api_key = (
    os.getenv("GOOGLE_API_KEY")
    or os.getenv("GEMINI_API_KEY")
    or os.getenv("OPENAI_API_KEY")
    or ""
)


try:
    import streamlit as st
    try:
        if not api_key:
            api_key = (
                st.secrets.get("GOOGLE_API_KEY")
                or st.secrets.get("GEMINI_API_KEY")
                or ""
            )
    except Exception:
        pass
except ImportError:
    st = None


if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key

# =====================================================================
# ३. Linux Disk 
# =====================================================================
secrets_toml_body = f"""GOOGLE_API_KEY = "{api_key}"
GEMINI_API_KEY = "{api_key}"

[default]
GOOGLE_API_KEY = "{api_key}"
GEMINI_API_KEY = "{api_key}"
"""

for target_dir in [
    Path("/root/.streamlit"),
    Path("/app/.streamlit"),
    Path.home() / ".streamlit",
    PROJECT_ROOT / ".streamlit",
]:
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "secrets.toml").write_text(secrets_toml_body.strip(), encoding="utf-8")
    except Exception:
        pass

# =====================================================================
# ४. Google Generative AI 
# =====================================================================
try:
    import google.generativeai as genai
    if api_key:
        genai.configure(api_key=api_key)
except Exception:
    pass

# =====================================================================
# ५. RAG Pipeline 
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
# ६. FastAPI Setup 
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
# 
# =====================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
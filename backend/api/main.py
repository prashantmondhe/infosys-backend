from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline

app = FastAPI(title="Enterprise RAG API Hub")

# Enable CORS for Next.js Frontend (Port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Pipeline Instance
pipeline = RAGPipeline()

# In-Memory Database for testing authentication & role mapping
users_db = {
    "admin@demo.com": {
        "name": "System Administrator",
        "password": "admin123",
        "role": "Admin"
    },
    "emp@demo.com": {
        "name": "Rohit",
        "password": "emp123",
        "role": "Employee"
    }
}

# Request Schemas
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str
    role: str

class QueryRequest(BaseModel):
    query: str
    designation: Optional[str] = "Software Engineer"

# 1. Register Endpoint
@app.post("/api/auth/register")
def register_user(payload: RegisterRequest):
    if payload.email in users_db:
        raise HTTPException(status_code=400, detail="User already registered with this email.")
    
    users_db[payload.email] = {
        "name": payload.name,
        "password": payload.password,
        "role": payload.role
    }
    return {"status": "success", "message": "Account created successfully."}

# 2. Login Endpoint
@app.post("/api/auth/login")
def login_user(payload: LoginRequest):
    user = users_db.get(payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    if user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid password.")
    if user["role"].lower() != payload.role.lower():
        raise HTTPException(status_code=403, detail=f"Access denied. Registered role is {user['role']}.")
    
    return {
        "status": "success",
        "name": user["name"],
        "email": payload.email,
        "role": user["role"]
    }

# 3. RAG AI Query Endpoint
@app.post("/api/rag/ask")
def ask_question(payload: QueryRequest):
    try:
        # If Admin, map to lead role for retrieval access
        mapped_role = "HR Operations Lead" if payload.designation == "Admin" else payload.designation
        result = pipeline.answer(query=payload.query, designation=mapped_role)
        
        # Format citations
        formatted_citations = []
        if hasattr(result, "citations") and result.citations:
            for item in result.citations:
                formatted_citations.append(getattr(item, "source", str(item)))

        return {
            "answer": result.answer,
            "citations": formatted_citations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
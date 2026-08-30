import os
from dataclasses import dataclass
from typing import Any, List
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
import google.generativeai as genai

try:
    import streamlit as st
except ImportError:
    st = None

from config.env_config import envConfig
from config.llm_config import (
    GEMINI_EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
)


@dataclass
class RetrievedEvidence:
    """
    Represents one piece of evidence retrieved from the vector database.
    """
    text: str
    score: float
    document_id: str
    chunk_id: str
    document_name: str
    page_number: int | None
    metadata: dict[str, Any]


# ----------------------------------------------------------------------
# 1. Official Google SDK वर आधारित Direct Embeddings Class
# (हा क्लास OAuth ऐवजी थेट API Key वापरतो, ज्यामुळे 401 एरर येत नाही)
# ----------------------------------------------------------------------
class DirectGeminiEmbeddings(Embeddings):
    def __init__(self, api_key: str, model_name: str = "models/text-embedding-004"):
        self.model_name = model_name
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            response = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            results.append(response['embedding'])
        return results

    def embed_query(self, text: str) -> List[float]:
        response = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_query"
        )
        return response['embedding']


# ----------------------------------------------------------------------
# 2. RAG Retriever Class
# ----------------------------------------------------------------------
class RAGRetriever:

    def __init__(
        self,
        vector_db_path: str | None = None,
        collection_name: str = "documents",
    ):
        if vector_db_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(
                os.path.join(script_dir, "..", "..", "..", "..")
            )
            vector_db_path = os.path.join(project_root, "vector_db")

        # API Key मिळवणे
        api_key = (
            (st.secrets.get("GEMINI_API_KEY") if st and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets else None)
            or (st.secrets.get("GOOGLE_API_KEY") if st and hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets else None)
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or getattr(envConfig, "GEMINI_API_KEY", None)
        )

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured in secrets or environment.")

        # डायरेक्ट गुगल एम्बेडिंग्स वापरणे
        self.embeddings = DirectGeminiEmbeddings(
            api_key=api_key,
            model_name=GEMINI_EMBEDDING_MODEL or "models/text-embedding-004"
        )

        # ChromaDB कनेक्शन
        self.vector_store = Chroma(
            persist_directory=vector_db_path,
            embedding_function=self.embeddings,
            collection_name=collection_name,
        )

    def retrieve(
        self,
        query: str,
        allowed_departments: list[str] | None = None,
        top_k: int = 20,
    ) -> list[RetrievedEvidence]:

        if not query or not query.strip() or top_k <= 0:
            return []

        search_kwargs: dict[str, Any] = {"k": top_k}

        if allowed_departments:
            search_kwargs["filter"] = {
                "department": {
                    "$in": allowed_departments,
                }
            }

        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                **search_kwargs,
            )
        except Exception:
            plain_docs = self.vector_store.similarity_search(
                query=query,
                **search_kwargs,
            )
            results = [(doc, 1.0) for doc in plain_docs]

        evidence: list[RetrievedEvidence] = []

        for item in results:
            if isinstance(item, (tuple, list)):
                document = item[0]
                raw_score = item[1] if len(item) > 1 else 1.0
            else:
                document = item
                raw_score = 1.0

            try:
                score = float(raw_score)
            except (ValueError, TypeError):
                score = 1.0

            metadata = document.metadata or {}

            document_id = str(metadata.get("document_id", ""))
            chunk_id = str(metadata.get("chunk_id", ""))
            document_name = str(
                metadata.get(
                    "title",
                    metadata.get("source_document", metadata.get("source", "Unknown document")),
                )
            )
            page_number = metadata.get("page_number")

            evidence.append(
                RetrievedEvidence(
                    text=document.page_content,
                    score=score,
                    document_id=document_id,
                    chunk_id=chunk_id,
                    document_name=document_name,
                    page_number=page_number,
                    metadata=metadata,
                )
            )

        return evidence
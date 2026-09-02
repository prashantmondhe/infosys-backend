import os
from dataclasses import dataclass
from typing import Any, List
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from google import genai
from google.genai import types

from backend.config.env_config import GEMINI_API_KEY, GOOGLE_API_KEY
from backend.config.llm_config import GEMINI_EMBEDDING_MODEL, EMBEDDING_DIMENSION


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
# Modern Google GenAI Client Embeddings (No OAuth Confusion)
# ----------------------------------------------------------------------
class DirectGenAIEmbeddings(Embeddings):
    def __init__(self, api_key: str, model_name: str = "text-embedding-004"):
        self.api_key = api_key
        # Clean model name if passed with 'models/' prefix
        self.model_name = model_name.replace("models/", "")
        self.client = genai.Client(api_key=self.api_key, vertexai=False)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            response = self.client.models.embed_content(
                model=self.model_name,
                contents=text,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
            )
            results.append(response.embedding.values)
        return results

    def embed_query(self, text: str) -> List[float]:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
        )
        return response.embedding.values


# ----------------------------------------------------------------------
# RAG Retriever
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

        # Key मिळवणे — st.secrets ला थेट टच करत नाही, त्यामुळे secrets.toml
        # नसतानाही क्रॅश होणार नाही
        api_key = GEMINI_API_KEY or GOOGLE_API_KEY

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        # आधुनिक Google SDK द्वारे Embeddings
        self.embeddings = DirectGenAIEmbeddings(
            api_key=api_key,
            model_name=GEMINI_EMBEDDING_MODEL
        )

        # ChromaDB इनिशियलायझेशन
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
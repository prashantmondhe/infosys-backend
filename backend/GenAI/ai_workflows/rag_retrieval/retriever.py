import os
from dataclasses import dataclass
from typing import Any
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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


class RAGRetriever:

    def __init__(
        self,
        vector_db_path: str | None = None,
        collection_name: str = "documents",
    ):

        if vector_db_path is None:

            script_dir = os.path.dirname(
                os.path.abspath(__file__)
            )

            project_root = os.path.abspath(
                os.path.join(
                    script_dir,
                    "..",
                    "..",
                    "..",
                    "..",
                )
            )

            vector_db_path = os.path.join(
                project_root,
                "vector_db",
            )

        # -------------------------------------------------
        # Gemini API key
        # -------------------------------------------------

        api_key = envConfig.GEMINI_API_KEY

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        # -------------------------------------------------
        # Gemini Embedding 2
        # -------------------------------------------------

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=GEMINI_EMBEDDING_MODEL,
            google_api_key=api_key,
            output_dimensionality=EMBEDDING_DIMENSION,
        )

        # -------------------------------------------------
        # ChromaDB
        # -------------------------------------------------

        self.vector_store = Chroma(
            persist_directory=vector_db_path,
            embedding_function=self.embeddings,
            collection_name=collection_name,
        )

    # =====================================================
    # Semantic retrieval
    # =====================================================

    def retrieve(
        self,
        query: str,
        allowed_departments: list[str] | None = None,
        top_k: int = 20,
    ) -> list[RetrievedEvidence]:

        if not query or not query.strip():
            return []

        if top_k <= 0:
            return []

        # -------------------------------------------------
        # Build metadata filter
        # -------------------------------------------------

        search_kwargs: dict[str, Any] = {
            "k": top_k,
        }

        if allowed_departments:

            search_kwargs["filter"] = {
                "department": {
                    "$in": allowed_departments,
                }
            }

        # -------------------------------------------------
        # Semantic similarity search with score
        # -------------------------------------------------

        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                **search_kwargs,
            )
        except Exception:
            # Fallback to plain similarity search if score method fails
            plain_docs = self.vector_store.similarity_search(
                query=query,
                **search_kwargs,
            )
            results = [(doc, 1.0) for doc in plain_docs]

        evidence: list[RetrievedEvidence] = []

        for item in results:
            # Safe unpacking: handles (doc, score) tuples or standalone Document objects
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

            document_id = str(
                metadata.get(
                    "document_id",
                    "",
                )
            )

            chunk_id = str(
                metadata.get(
                    "chunk_id",
                    "",
                )
            )

            document_name = str(
                metadata.get(
                    "title",
                    metadata.get(
                        "source_document",
                        metadata.get("source", "Unknown document"),
                    ),
                )
            )

            page_number = metadata.get(
                "page_number"
            )

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
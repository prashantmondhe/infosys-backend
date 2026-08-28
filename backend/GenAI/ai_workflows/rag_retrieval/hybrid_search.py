import re
from rank_bm25 import BM25Okapi
from .retriever import RAGRetriever, RetrievedEvidence


class HybridSearch:
    """
    Genuine hybrid retrieval using:

    1. Gemini Embedding 2 semantic search
    2. BM25 lexical search
    3. Reciprocal Rank Fusion (RRF)

    Semantic search handles meaning and paraphrases.

    BM25 handles exact terms, document IDs, project names,
    acronyms, policy numbers, technical terms, etc.
    """

    def __init__(
        self,
        retriever: RAGRetriever,
        semantic_top_k: int = 50,
        lexical_top_k: int = 50,
        rrf_k: int = 60,
    ):
        self.retriever = retriever

        self.semantic_top_k = semantic_top_k
        self.lexical_top_k = lexical_top_k
        self.rrf_k = rrf_k

    # =====================================================
    # BM25 INDEX
    # =====================================================

    def _build_bm25_index(
        self,
        allowed_departments: list[str] | None = None,
    ):
        """
        Build a BM25 index from chunks stored in Chroma.

        RBAC filtering is applied before creating the lexical index.
        """

        collection = self.retriever.vector_store._collection

        where_filter = None

        if allowed_departments:
            where_filter = {
                "department": {
                    "$in": allowed_departments
                }
            }

        data = collection.get(
            where=where_filter,
            include=[
                "documents",
                "metadatas",
            ],
        )

        documents = data.get("documents") or []
        metadatas = data.get("metadatas") or []

        if not documents:
            return None, [], []

        tokenized_documents = [
            self._tokenize(document)
            for document in documents
        ]

        # Remove completely empty documents.
        valid_documents = []
        valid_metadatas = []
        tokenized_valid_documents = []

        for document, metadata, tokens in zip(
            documents,
            metadatas,
            tokenized_documents,
        ):
            if not tokens:
                continue

            valid_documents.append(document)
            valid_metadatas.append(metadata)
            tokenized_valid_documents.append(tokens)

        if not valid_documents:
            return None, [], []

        bm25 = BM25Okapi(
            tokenized_valid_documents
        )

        return (
            bm25,
            valid_documents,
            valid_metadatas,
        )

    # =====================================================
    # TOKENIZATION
    # =====================================================

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """
        Tokenize text while preserving enterprise identifiers.

        Examples preserved as useful tokens:

            HR-2026-001
            API-GATEWAY
            Project_X
            ISO-27001
            SLA-001
        """

        if not text:
            return []

        text = text.lower()

        return re.findall(
            r"[a-z0-9]+(?:[-_][a-z0-9]+)*",
            text,
        )

    # =====================================================
    # LEXICAL SEARCH
    # =====================================================

    def _lexical_search(
        self,
        query: str,
        allowed_departments: list[str] | None = None,
    ) -> list[RetrievedEvidence]:

        (
            bm25,
            documents,
            metadatas,
        ) = self._build_bm25_index(
            allowed_departments=allowed_departments,
        )

        if bm25 is None:
            return []

        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        scores = bm25.get_scores(
            query_tokens
        )

        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indexes:

            score = float(scores[index])

            # No lexical match.
            if score <= 0:
                continue

            metadata = metadatas[index] or {}

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
                        "Unknown document",
                    ),
                )
            )

            results.append(
                RetrievedEvidence(
                    text=documents[index],
                    score=score,
                    document_id=document_id,
                    chunk_id=chunk_id,
                    document_name=document_name,
                    page_number=metadata.get(
                        "page_number"
                    ),
                    metadata=metadata,
                )
            )

            if len(results) >= self.lexical_top_k:
                break

        return results

    # =====================================================
    # RECIPROCAL RANK FUSION
    # =====================================================

    def _rrf_fusion(
        self,
        semantic_results: list[RetrievedEvidence],
        lexical_results: list[RetrievedEvidence],
    ) -> list[RetrievedEvidence]:
        """
        Combine semantic and lexical rankings using RRF.

        RRF score:

            1 / (rrf_k + rank)
        """

        rrf_scores: dict[str, float] = {}

        evidence_map: dict[
            str,
            RetrievedEvidence,
        ] = {}

        # ---------------------------------------------
        # Semantic ranking
        # ---------------------------------------------

        for rank, evidence in enumerate(
            semantic_results,
            start=1,
        ):

            chunk_id = evidence.chunk_id

            if not chunk_id:
                continue

            rrf_scores[chunk_id] = (
                rrf_scores.get(
                    chunk_id,
                    0.0,
                )
                + 1.0
                / (
                    self.rrf_k + rank
                )
            )

            evidence_map[chunk_id] = evidence

        # ---------------------------------------------
        # BM25 ranking
        # ---------------------------------------------

        for rank, evidence in enumerate(
            lexical_results,
            start=1,
        ):

            chunk_id = evidence.chunk_id

            if not chunk_id:
                continue

            rrf_scores[chunk_id] = (
                rrf_scores.get(
                    chunk_id,
                    0.0,
                )
                + 1.0
                / (
                    self.rrf_k + rank
                )
            )

            # If semantic search already found this chunk,
            # keep its complete evidence object.
            if chunk_id not in evidence_map:
                evidence_map[chunk_id] = evidence

        # ---------------------------------------------
        # Final ranking
        # ---------------------------------------------

        ranked_chunk_ids = sorted(
            rrf_scores.keys(),
            key=lambda chunk_id: rrf_scores[
                chunk_id
            ],
            reverse=True,
        )

        results = []

        for chunk_id in ranked_chunk_ids:

            evidence = evidence_map[chunk_id]

            # Replace the original score with
            # the fused RRF score.
            evidence.score = rrf_scores[
                chunk_id
            ]

            results.append(evidence)

        return results

    # =====================================================
    # PUBLIC SEARCH
    # =====================================================

    def search(
        self,
        query: str,
        allowed_departments: list[str] | None = None,
        top_k: int = 20,
    ) -> list[RetrievedEvidence]:

        if not query or not query.strip():
            return []

        if top_k <= 0:
            return []

        # ---------------------------------------------
        # 1. Semantic retrieval
        # ---------------------------------------------

        semantic_results = (
            self.retriever.retrieve(
                query=query,
                allowed_departments=allowed_departments,
                top_k=self.semantic_top_k,
            )
        )

        # ---------------------------------------------
        # 2. BM25 lexical retrieval
        # ---------------------------------------------

        lexical_results = (
            self._lexical_search(
                query=query,
                allowed_departments=allowed_departments,
            )
        )

        # ---------------------------------------------
        # 3. RRF fusion
        # ---------------------------------------------

        fused_results = self._rrf_fusion(
            semantic_results=semantic_results,
            lexical_results=lexical_results,
        )

        # ---------------------------------------------
        # 4. Return top-K
        # ---------------------------------------------

        return fused_results[:top_k]
from pydantic import BaseModel, Field
from config.llm_config import client, GEMINI_MODEL
from .retriever import RetrievedEvidence


class RankedEvidence(BaseModel):
    chunk_id: str = Field(
        description="ID of the retrieved chunk."
    )

    relevance_score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "How strongly this chunk supports "
            "answering the query."
        ),
    )


class RerankerResponse(BaseModel):
    results: list[RankedEvidence]


class EvidenceReranker:

    def __init__(
        self,
        final_top_k: int = 6,
    ):
        if final_top_k <= 0:
            raise ValueError(
                "final_top_k must be greater than zero."
            )

        self.final_top_k = final_top_k

    def rerank(
        self,
        query: str,
        evidence: list[RetrievedEvidence],
    ) -> list[RetrievedEvidence]:

        if not query or not query.strip():
            return []

        if not evidence:
            return []

        # -------------------------------------------------
        # Remove duplicate chunks
        # -------------------------------------------------

        unique_evidence = {}

        for item in evidence:

            if not item.chunk_id:
                continue

            if item.chunk_id not in unique_evidence:
                unique_evidence[item.chunk_id] = item

        evidence = list(
            unique_evidence.values()
        )

        if not evidence:
            return []

        # -------------------------------------------------
        # Build reranking candidates
        # -------------------------------------------------

        candidates = "\n\n".join(
            f"""
CHUNK_ID: {item.chunk_id}
DOCUMENT: {item.document_name}
PAGE: {item.page_number}

CONTENT:
{item.text}
"""
            for item in evidence
        )

        # -------------------------------------------------
        # Reranking prompt
        # -------------------------------------------------

        prompt = f"""
You are an enterprise RAG evidence reranker.

USER QUERY:
{query}

RETRIEVED CANDIDATES:
{candidates}

Evaluate each candidate based on how useful it is
for answering the user's query.

RULES:

1. Rank candidates by direct relevance.
2. Prefer evidence that directly answers the query.
3. Do not reward a chunk merely because it shares
   related words with the query.
4. Prefer specific evidence over generic information.
5. Do not use outside knowledge.
6. Return ONLY chunk IDs that were provided above.
7. Never invent a chunk ID.
8. Assign every returned chunk a score between 0 and 1.
9. Higher score means stronger evidence.
10. Return the strongest candidates first.
"""

        # -------------------------------------------------
        # Gemini reranking
        # -------------------------------------------------

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": RerankerResponse,
            },
        )

        ranked = (
            RerankerResponse.model_validate_json(
                response.text
            )
        )

        # -------------------------------------------------
        # Map retrieved evidence
        # -------------------------------------------------

        evidence_map = {
            item.chunk_id: item
            for item in evidence
        }

        final_results = []
        seen_chunk_ids = set()

        # -------------------------------------------------
        # Validate Gemini output
        # -------------------------------------------------

        for result in ranked.results:

            chunk_id = result.chunk_id

            # Reject hallucinated chunk IDs.
            item = evidence_map.get(chunk_id)

            if item is None:
                continue

            # Reject duplicate chunks.
            if chunk_id in seen_chunk_ids:
                continue

            seen_chunk_ids.add(chunk_id)

            # Keep original retrieval/RRF score.
            # Store reranker score separately.
            item.rerank_score = (
                result.relevance_score
            )

            final_results.append(item)

            if len(final_results) >= self.final_top_k:
                break

        return final_results
    
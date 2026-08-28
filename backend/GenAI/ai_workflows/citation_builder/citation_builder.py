from dataclasses import dataclass
from ..grounded_synthesis.synthesis_engine import SynthesisResponse
from ..rag_retrieval.retriever import RetrievedEvidence


@dataclass
class Citation:
    citation_id: int
    document_id: str
    document_name: str
    page_number: int | None
    chunk_id: str
    text: str


@dataclass
class CitedClaim:
    claim: str
    citations: list[Citation]


class CitationBuilder:
    """
    Converts Gemini evidence references (E1, E2, ...)
    into citations using the actual retrieved evidence.

    Gemini never generates the citation metadata.
    """

    def build(
        self,
        synthesis: SynthesisResponse,
        evidence: list[RetrievedEvidence],
    ) -> list[CitedClaim]:

        # Map E1, E2, E3... to actual retrieved evidence.
        evidence_map = {
            f"E{index}": item
            for index, item in enumerate(
                evidence,
                start=1,
            )
        }

        # Keep citations unique by chunk.
        citation_map: dict[str, Citation] = {}

        cited_claims: list[CitedClaim] = []

        for claim in synthesis.claims:

            claim_citations: list[Citation] = []

            for evidence_id in claim.evidence_ids:

                item = evidence_map.get(evidence_id)

                # Ignore invalid evidence references.
                if item is None:
                    continue

                # One citation per unique chunk.
                if item.chunk_id not in citation_map:

                    citation_map[item.chunk_id] = Citation(
                        citation_id=len(citation_map) + 1,
                        document_id=item.document_id,
                        document_name=item.document_name,
                        page_number=item.page_number,
                        chunk_id=item.chunk_id,
                        text=item.text,
                    )

                claim_citations.append(
                    citation_map[item.chunk_id]
                )

            # Only include claims that have valid citations.
            if claim_citations:

                cited_claims.append(
                    CitedClaim(
                        claim=claim.claim,
                        citations=claim_citations,
                    )
                )

        return cited_claims
from dataclasses import dataclass
from .citation_builder import CitedClaim


@dataclass
class FormattedCitation:
    citation_id: int
    document_id: str
    document_name: str
    page_number: int | None
    chunk_id: str


@dataclass
class FormattedResponse:
    answer: str
    citations: list[FormattedCitation]


class CitationFormatter:
    """
    Formats validated claims and deterministic citations
    into the final clean response without duplicate tags.
    """

    def format(
        self,
        cited_claims: list[CitedClaim],
    ) -> FormattedResponse:

        if not cited_claims:
            return FormattedResponse(
                answer=(
                    "I couldn't find sufficient verified "
                    "evidence to answer this question."
                ),
                citations=[],
            )

        citation_map: dict[int, FormattedCitation] = {}
        answer_parts: list[str] = []

        for claim in cited_claims:
            if not claim.citations:
                continue

            unique_citation_ids: list[int] = []

            for citation in claim.citations:
                if citation.citation_id not in citation_map:
                    citation_map[citation.citation_id] = FormattedCitation(
                        citation_id=citation.citation_id,
                        document_id=citation.document_id,
                        document_name=citation.document_name,
                        page_number=citation.page_number,
                        chunk_id=citation.chunk_id,
                    )

                if citation.citation_id not in unique_citation_ids:
                    unique_citation_ids.append(citation.citation_id)

            if not unique_citation_ids:
                continue

            unique_citation_ids.sort()

            formatted_refs = f"[{', '.join(str(cid) for cid in unique_citation_ids)}]"

            claim_text = claim.claim.strip()
        
            if claim_text.endswith("."):
                claim_text = claim_text[:-1].strip()
                answer_parts.append(f"{claim_text} {formatted_refs}.")
            else:
                answer_parts.append(f"{claim_text} {formatted_refs}")

     
        if not answer_parts:
            return FormattedResponse(
                answer=(
                    "I couldn't find sufficient verified "
                    "evidence to answer this question."
                ),
                citations=[],
            )

        return FormattedResponse(
            answer="\n\n".join(answer_parts),
            citations=list(citation_map.values()),
        )
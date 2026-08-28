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
    into the final response.

    This class only formats the response.
    It does not generate or validate citations.
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

            citation_numbers: list[int] = []

            for citation in claim.citations:

                if citation.citation_id not in citation_map:

                    citation_map[
                        citation.citation_id
                    ] = FormattedCitation(
                        citation_id=citation.citation_id,
                        document_id=citation.document_id,
                        document_name=citation.document_name,
                        page_number=citation.page_number,
                        chunk_id=citation.chunk_id,
                    )

                citation_numbers.append(
                    citation.citation_id
                )

            references = " ".join(
                f"[{number}]"
                for number in citation_numbers
            )

            answer_parts.append(
                f"{claim.claim} {references}"
            )

        # All claims were missing usable citations.
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
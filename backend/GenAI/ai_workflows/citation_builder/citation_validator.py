from dataclasses import dataclass
from ..grounded_synthesis.synthesis_engine import SynthesisResponse
from ..rag_retrieval.retriever import RetrievedEvidence


@dataclass
class ValidatedClaim:
    claim: str
    evidence_ids: list[str]
    is_valid: bool
    reason: str | None = None


class CitationValidator:

    def validate(
        self,
        synthesis: SynthesisResponse,
        evidence: list[RetrievedEvidence],
    ) -> list[ValidatedClaim]:

        # E1, E2, E3... → actual retrieved evidence
        evidence_map = {
            f"E{index}": item
            for index, item in enumerate(
                evidence,
                start=1,
            )
        }

        validated_claims = []

        for claim in synthesis.claims:

            # -----------------------------------------
            # 1. Claim must have evidence
            # -----------------------------------------

            if not claim.evidence_ids:
                validated_claims.append(
                    ValidatedClaim(
                        claim=claim.claim,
                        evidence_ids=[],
                        is_valid=False,
                        reason="Claim has no supporting evidence.",
                    )
                )
                continue

            # -----------------------------------------
            # 2. Every evidence ID must exist
            # -----------------------------------------

            invalid_ids = [
                evidence_id
                for evidence_id in claim.evidence_ids
                if evidence_id not in evidence_map
            ]

            if invalid_ids:
                validated_claims.append(
                    ValidatedClaim(
                        claim=claim.claim,
                        evidence_ids=claim.evidence_ids,
                        is_valid=False,
                        reason=(
                            f"Unknown evidence IDs: "
                            f"{', '.join(invalid_ids)}"
                        ),
                    )
                )
                continue

            # -----------------------------------------
            # 3. Evidence exists
            # -----------------------------------------

            validated_claims.append(
                ValidatedClaim(
                    claim=claim.claim,
                    evidence_ids=claim.evidence_ids,
                    is_valid=True,
                )
            )

        return validated_claims
from pydantic import BaseModel, Field
from config.llm_config import client, GEMINI_MODEL
from ..rag_retrieval.retriever import RetrievedEvidence


MIN_SUPPORT_SCORE = 0.80


class ClaimVerification(BaseModel):
    supported: bool = Field(
        description="Whether the evidence directly supports the claim."
    )

    support_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Strength of evidence support."
    )

    reason: str = Field(
        description="Short explanation for the verification decision."
    )


class BatchClaimVerification(BaseModel):
    verifications: list[ClaimVerification] = Field(
        description=(
            "Verification result for each claim, in exactly "
            "the same order as the supplied claims."
        )
    )


class ClaimVerifier:

    # =================================================
    # Single claim verification
    # =================================================

    def verify(
        self,
        claim: str,
        evidence: list[RetrievedEvidence],
        evidence_ids: list[str],
    ) -> ClaimVerification:

        evidence_map = {
            f"E{index}": item
            for index, item in enumerate(
                evidence,
                start=1,
            )
        }

        selected_evidence = []

        for evidence_id in evidence_ids:

            item = evidence_map.get(evidence_id)

            if item is not None:

                selected_evidence.append(
                    f"""
[{evidence_id}]
Document: {item.document_name}
Page: {item.page_number}

Evidence:
{item.text}
"""
                )

        if not selected_evidence:

            return ClaimVerification(
                supported=False,
                support_score=0.0,
                reason="No valid evidence was provided.",
            )

        context = "\n".join(selected_evidence)

        prompt = f"""
You are an evidence verification system for an enterprise RAG application.

CLAIM:
{claim}

EVIDENCE:
{context}

Determine whether the supplied evidence directly supports the claim.

Rules:
- Use ONLY the supplied evidence.
- Do not use outside knowledge.
- Do not assume missing information.
- The evidence must actually support the claim.
- If the evidence only discusses a related topic but does not support
  the claim, mark it unsupported.
- A contradiction must be marked unsupported.
- Give a score between 0 and 1.
- Score 1.0 means the evidence directly and clearly supports the claim.
- Score 0.0 means there is no support.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ClaimVerification,
            },
        )

        result = ClaimVerification.model_validate_json(
            response.text
        )

        if result.support_score < MIN_SUPPORT_SCORE:
            result.supported = False

        return result

    # =================================================
    # Batch claim verification
    # =================================================

    def verify_batch(
        self,
        claims: list[tuple[str, list[str]]],
        evidence: list[RetrievedEvidence],
    ) -> list[ClaimVerification]:

        if not claims:

            return []

        evidence_map = {
            f"E{index}": item
            for index, item in enumerate(
                evidence,
                start=1,
            )
        }

        claim_blocks = []

        for index, (claim, evidence_ids) in enumerate(
            claims,
            start=1,
        ):

            selected_evidence = []

            for evidence_id in evidence_ids:

                item = evidence_map.get(evidence_id)

                if item is not None:

                    selected_evidence.append(
                        f"""
[{evidence_id}]
Document: {item.document_name}
Page: {item.page_number}

Evidence:
{item.text}
"""
                    )

            if selected_evidence:

                evidence_text = "\n".join(
                    selected_evidence
                )

            else:

                evidence_text = (
                    "NO VALID EVIDENCE PROVIDED."
                )

            claim_blocks.append(
                f"""
CLAIM {index}:
{claim}

SUPPORTING EVIDENCE:
{evidence_text}
"""
            )

        context = "\n".join(claim_blocks)

        prompt = f"""
You are an evidence verification system for an enterprise RAG application.

Verify each claim independently against ONLY its supplied evidence.

{context}

RULES:

1. Use ONLY the supplied evidence.
2. Do not use outside knowledge.
3. Do not assume missing information.
4. Each claim must be evaluated independently.
5. The evidence must directly support the claim.
6. Related evidence that does not actually support the claim
   must be marked unsupported.
7. A contradiction must be marked unsupported.
8. Score each claim from 0.0 to 1.0.
9. 1.0 means the evidence directly and clearly supports the claim.
10. 0.0 means there is no support.
11. Return exactly ONE verification result for every claim.
12. Preserve the exact claim order.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": BatchClaimVerification,
            },
        )

        result = (
            BatchClaimVerification
            .model_validate_json(response.text)
        )

        verifications = result.verifications

        # ---------------------------------------------
        # Safety: ensure result count matches claims
        # ---------------------------------------------

        if len(verifications) != len(claims):

            return [
                ClaimVerification(
                    supported=False,
                    support_score=0.0,
                    reason=(
                        "Batch verification returned an "
                        "unexpected number of results."
                    ),
                )
                for _ in claims
            ]

        # ---------------------------------------------
        # Application-level threshold
        # ---------------------------------------------

        for verification in verifications:

            if (
                verification.support_score
                < MIN_SUPPORT_SCORE
            ):

                verification.supported = False

        return verifications
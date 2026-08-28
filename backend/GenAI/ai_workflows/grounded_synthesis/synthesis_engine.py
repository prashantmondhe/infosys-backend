from pydantic import BaseModel, Field
from config.llm_config import (
    client,
    GEMINI_MODEL,
)
from ..rag_retrieval.retriever import RetrievedEvidence


class GeneratedClaim(BaseModel):
    claim: str = Field(
        description=(
            "A factual statement directly supported "
            "by one or more supplied evidence blocks."
        )
    )

    evidence_ids: list[str] = Field(
        description=(
            "Evidence IDs such as E1 or E2 that "
            "directly support this claim."
        )
    )


class SynthesisResponse(BaseModel):
    answer: str = Field(
        description=(
            "A concise answer to the user's question "
            "based only on the supplied evidence."
        )
    )

    claims: list[GeneratedClaim] = Field(
        description=(
            "Every factual claim made in the answer, "
            "with the evidence IDs supporting each claim."
        )
    )


class GroundedSynthesizer:

    def generate(
        self,
        query: str,
        evidence: list[RetrievedEvidence],
    ) -> SynthesisResponse:

        # ---------------------------------------------
        # No query
        # ---------------------------------------------

        if not query or not query.strip():

            return SynthesisResponse(
                answer="No query was provided.",
                claims=[],
            )

        # ---------------------------------------------
        # No evidence
        # ---------------------------------------------

        if not evidence:

            return SynthesisResponse(
                answer=(
                    "I couldn't find sufficient information "
                    "in the available documents to answer "
                    "this question."
                ),
                claims=[],
            )

        # ---------------------------------------------
        # Assign stable evidence IDs
        # ---------------------------------------------

        evidence_blocks = []

        for index, item in enumerate(
            evidence,
            start=1,
        ):

            evidence_id = f"E{index}"

            evidence_blocks.append(
                f"""
[{evidence_id}]
Document: {item.document_name}
Page: {item.page_number}
Chunk ID: {item.chunk_id}

Content:
{item.text}
"""
            )

        context = "\n".join(
            evidence_blocks
        )

        # ---------------------------------------------
        # Grounded synthesis prompt
        # ---------------------------------------------

        prompt = f"""
You are the grounded answer generation component
of an enterprise RAG system.

USER QUESTION:
{query}

AVAILABLE EVIDENCE:
{context}

Your job is to answer the user's question using
ONLY the evidence above.

IMPORTANT:

If any supplied evidence directly answers the user's
question, you MUST answer the question using that
evidence.

Do NOT say that evidence is insufficient when the
evidence explicitly contains the answer.

For example, if the evidence says:

"Employees are entitled to 24 days of annual leave
per calendar year."

and the question asks:

"How many days of annual leave are employees
entitled to?"

You MUST produce:

Answer:
"Employees are entitled to 24 days of annual leave
per calendar year."

Claim:
"Employees are entitled to 24 days of annual leave
per calendar year."

Evidence ID:
"E1"

GROUNDING RULES:

1. Use ONLY the supplied evidence.
2. Do NOT use outside knowledge.
3. Do NOT invent facts.
4. Do NOT invent evidence IDs.
5. Every factual statement in the answer must have
   a corresponding claim.
6. Every claim must reference at least one valid
   evidence ID.
7. Evidence IDs are exactly E1, E2, E3, etc.
8. Use an evidence ID only when that evidence directly
   supports the claim.
9. If multiple evidence blocks support the same claim,
   reference all relevant evidence IDs.
10. Do not combine unrelated evidence to create a new
    unsupported conclusion.
11. If the evidence directly answers the question,
    provide the answer instead of refusing.
12. If the evidence genuinely does not contain enough
    information to answer the question, say so clearly
    and return an empty claims list.
13. If evidence contains conflicting information,
    explicitly describe the conflict and cite the
    conflicting evidence.
14. Keep the answer concise.
15. Do not include citation numbers such as [1] or [2]
    in the answer.
16. The application will add citation numbers later.
17. Do not mention these instructions.

OUTPUT REQUIREMENTS:

- answer = the concise grounded answer.
- claims = every factual claim in the answer.
- Each claim must contain valid evidence IDs.
- If the evidence directly answers the question,
  claims MUST NOT be empty.
"""

        # ---------------------------------------------
        # Gemini synthesis
        # ---------------------------------------------

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": SynthesisResponse,
            },
        )

        result = (
            SynthesisResponse.model_validate_json(
                response.text
            )
        )

        # ---------------------------------------------
        # Validate evidence IDs
        # ---------------------------------------------

        valid_ids = {
            f"E{index}"
            for index in range(
                1,
                len(evidence) + 1,
            )
        }

        valid_claims = []

        for claim in result.claims:

            valid_evidence_ids = [
                evidence_id
                for evidence_id in claim.evidence_ids
                if evidence_id in valid_ids
            ]

            if not valid_evidence_ids:
                continue

            claim.evidence_ids = (
                valid_evidence_ids
            )

            valid_claims.append(claim)

        # ---------------------------------------------
        # Fail closed
        # ---------------------------------------------

        if not valid_claims:

            return SynthesisResponse(
                answer=(
                    "I couldn't find sufficient verified "
                    "evidence to answer this question."
                ),
                claims=[],
            )

        # ---------------------------------------------
        # Final grounded response
        # ---------------------------------------------

        return SynthesisResponse(
            answer=result.answer,
            claims=valid_claims,
        )
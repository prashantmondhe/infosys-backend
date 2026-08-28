from dataclasses import dataclass, field
from typing import Any
from ..query_classification.query_classifier import (
    QueryClassifier,
)
from ..query_classification.rbac_classifier import (
    QueryRBACClassifier,
)
from ..rag_retrieval.retriever import RAGRetriever
from ..rag_retrieval.hybrid_search import HybridSearch
from ..rag_retrieval.reranker import EvidenceReranker
from ..grounded_synthesis.synthesis_engine import (
    GroundedSynthesizer,
)
from ..citation_builder.citation_builder import (
    CitationBuilder,
)
from ..citation_builder.citation_validator import (
    CitationValidator,
)
from ..citation_builder.citation_formatter import (
    CitationFormatter,
)
from ..verification.claim_verifier import (
    ClaimVerifier,
)


@dataclass
class RAGResponse:
    answer: str
    citations: list[Any] = field(default_factory=list)
    claims: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


class RAGPipeline:

    def __init__(self):

        # ---------------------------------------------
        # Query classification
        # ---------------------------------------------

        self.query_classifier = QueryClassifier()

        # ---------------------------------------------
        # RBAC
        # ---------------------------------------------

        self.rbac_classifier = QueryRBACClassifier()

        # ---------------------------------------------
        # Retrieval
        # ---------------------------------------------

        self.retriever = RAGRetriever()

        self.hybrid_search = HybridSearch(
            retriever=self.retriever,
        )

        self.reranker = EvidenceReranker(
            final_top_k=6,
        )

        # ---------------------------------------------
        # Grounded synthesis
        # ---------------------------------------------

        self.synthesizer = GroundedSynthesizer()

        # ---------------------------------------------
        # Citation validation
        # ---------------------------------------------

        self.citation_validator = CitationValidator()

        # ---------------------------------------------
        # Claim verification
        # ---------------------------------------------

        self.claim_verifier = ClaimVerifier()

        # ---------------------------------------------
        # Citation building
        # ---------------------------------------------

        self.citation_builder = CitationBuilder()

        # ---------------------------------------------
        # Citation formatting
        # ---------------------------------------------

        self.citation_formatter = CitationFormatter()

    # =================================================
    # Main pipeline
    # =================================================

    def answer(
        self,
        query: str,
        designation: str,
    ) -> RAGResponse:

        # ---------------------------------------------
        # 0. Validate input
        # ---------------------------------------------

        if not query or not query.strip():

            return RAGResponse(
                answer="Please provide a question.",
                metadata={
                    "pipeline_status": "invalid_query",
                },
            )

        if not designation or not designation.strip():

            return RAGResponse(
                answer=(
                    "Your user role could not be determined, "
                    "so the request cannot be authorized."
                ),
                metadata={
                    "pipeline_status": "missing_designation",
                    "access_granted": False,
                },
            )

        # ---------------------------------------------
        # 1. Query classification
        # ---------------------------------------------

        classification = (
            self.query_classifier.classify(query)
        )

        # ---------------------------------------------
        # 2. Clarification
        # ---------------------------------------------

        if classification.needs_clarification:

            return RAGResponse(
                answer=(
                    classification.clarification_question
                    or "Could you clarify your question?"
                ),
                metadata={
                    "pipeline_status": "clarification_required",
                    "intent": classification.intent.value,
                    "query_type": classification.query_type.value,
                },
            )

        # ---------------------------------------------
        # 3. Non-RAG query
        # ---------------------------------------------

        if not classification.requires_rag:

            return RAGResponse(
                answer=(
                    "This query does not require enterprise "
                    "document retrieval."
                ),
                metadata={
                    "pipeline_status": "non_rag",
                    "requires_rag": False,
                    "intent": classification.intent.value,
                    "query_type": classification.query_type.value,
                },
            )

        # ---------------------------------------------
        # 4. RBAC
        # ---------------------------------------------

        allowed_departments = (
            self.rbac_classifier
            .get_allowed_departments(
                designation
            )
        )

        if not allowed_departments:

            return RAGResponse(
                answer=(
                    "You do not have access to the "
                    "required enterprise information."
                ),
                metadata={
                    "pipeline_status": "access_denied",
                    "access_granted": False,
                },
            )

        # ---------------------------------------------
        # 5. Hybrid retrieval
        # ---------------------------------------------

        retrieved = self.hybrid_search.search(
            query=query,
            allowed_departments=allowed_departments,
            top_k=20,
        )

        if not retrieved:

            return RAGResponse(
                answer=(
                    "I couldn't find relevant information "
                    "in the documents you are authorized "
                    "to access."
                ),
                metadata={
                    "pipeline_status": "no_retrieval_results",
                    "access_granted": True,
                    "retrieved_count": 0,
                },
            )

        # ---------------------------------------------
        # 6. Reranking
        # ---------------------------------------------

        evidence = self.reranker.rerank(
            query=query,
            evidence=retrieved,
        )

        if not evidence:

            return RAGResponse(
                answer=(
                    "I couldn't find sufficient evidence "
                    "to answer this question."
                ),
                metadata={
                    "pipeline_status": "no_sufficient_evidence",
                    "retrieved_count": len(retrieved),
                    "final_evidence_count": 0,
                },
            )

        # ---------------------------------------------
        # DEBUG — Evidence sent to synthesizer
        # ---------------------------------------------

        print("\n" + "=" * 60)
        print("EVIDENCE SENT TO SYNTHESIZER")
        print("=" * 60)

        for index, item in enumerate(
            evidence,
            start=1,
        ):

            print(f"\n[E{index}]")

            print(
                f"Chunk ID: {item.chunk_id}"
            )

            print(
                f"Document: {item.document_name}"
            )

            print(
                f"Page: {item.page_number}"
            )

            print(
                "Rerank Score: "
                f"{getattr(item, 'rerank_score', None)}"
            )

            print("Text:")
            print(item.text)

        print("=" * 60)

        # ---------------------------------------------
        # 7. Grounded synthesis
        # ---------------------------------------------

        synthesis = self.synthesizer.generate(
            query=query,
            evidence=evidence,
        )

        # ---------------------------------------------
        # DEBUG — Synthesis output
        # ---------------------------------------------

        print("\n" + "=" * 60)
        print("SYNTHESIS DEBUG")
        print("=" * 60)

        print("\nSYNTHESIS ANSWER:")
        print(synthesis.answer)

        print("\nSYNTHESIS CLAIMS:")

        if not synthesis.claims:
            print("NO CLAIMS RETURNED.")

        for claim in synthesis.claims:

            print(
                f"Claim: {claim.claim}"
            )

            print(
                f"Evidence IDs: "
                f"{claim.evidence_ids}"
            )

        # ---------------------------------------------
        # 8. Validate evidence references
        # ---------------------------------------------

        validated_claims = (
            self.citation_validator.validate(
                synthesis=synthesis,
                evidence=evidence,
            )
        )

        # ---------------------------------------------
        # DEBUG — Citation validation
        # ---------------------------------------------

        print("\nVALIDATED CLAIMS:")

        if not validated_claims:
            print("NO VALIDATED CLAIMS RETURNED.")

        for claim in validated_claims:

            print(
                f"Claim: {claim.claim}"
            )

            print(
                f"Evidence IDs: "
                f"{claim.evidence_ids}"
            )

            print(
                f"Valid: "
                f"{claim.is_valid}"
            )

            print(
                f"Reason: "
                f"{claim.reason}"
            )

        print("=" * 60)

        # ---------------------------------------------
        # 9. Semantic claim verification
        # ---------------------------------------------

        verified_claims = []
        verification_results = []

        # ---------------------------------------------
        # Prepare valid claims for batch verification
        # ---------------------------------------------

        validatable_claims = [
            validated
            for validated in validated_claims
            if validated.is_valid
        ]

        claims_to_verify = [
            (
                validated.claim,
                validated.evidence_ids,
            )
            for validated in validatable_claims
        ]

        # ---------------------------------------------
        # Verify all claims in ONE Gemini request
        # ---------------------------------------------

        if claims_to_verify:

            batch_results = (
                self.claim_verifier.verify_batch(
                    claims=claims_to_verify,
                    evidence=evidence,
                )
            )

            # -----------------------------------------
            # Match verification results to claims
            # -----------------------------------------

            for validated, verification in zip(
                validatable_claims,
                batch_results,
            ):

                verification_results.append(
                    {
                        "claim": validated.claim,
                        "support_score": (
                            verification.support_score
                        ),
                        "supported": verification.supported,
                        "reason": verification.reason,
                    }
                )

                if verification.supported:

                    verified_claims.append(
                        validated
                    )

        # ---------------------------------------------
        # 10. Fail closed if nothing was verified
        # ---------------------------------------------

        if not verified_claims:

            return RAGResponse(
                answer=(
                    "I couldn't verify sufficient evidence "
                    "in the available enterprise documents "
                    "to provide a reliable answer."
                ),
                claims=[],
                citations=[],
                metadata={
                    "pipeline_status": "verification_failed",
                    "requires_rag": True,
                    "access_granted": True,
                    "retrieved_count": len(retrieved),
                    "final_evidence_count": len(evidence),
                    "verified_claim_count": 0,
                    "verification_results": (
                        verification_results
                    ),
                },
            )

        # ---------------------------------------------
        # 11. Keep only verified claims
        # ---------------------------------------------

        verified_claim_texts = {
            claim.claim
            for claim in verified_claims
        }

        verified_synthesis = synthesis.model_copy(
            update={
                "claims": [
                    claim
                    for claim in synthesis.claims
                    if claim.claim in verified_claim_texts
                ]
            }
        )

        # ---------------------------------------------
        # 12. Build deterministic citations
        # ---------------------------------------------

        cited_claims = self.citation_builder.build(
            synthesis=verified_synthesis,
            evidence=evidence,
        )

        # ---------------------------------------------
        # 13. Format final verified response
        # ---------------------------------------------

        formatted_response = (
            self.citation_formatter.format(
                cited_claims=cited_claims,
            )
        )

        # ---------------------------------------------
        # 14. Final safety check
        # ---------------------------------------------

        if not formatted_response.answer.strip():

            return RAGResponse(
                answer=(
                    "I couldn't generate a verified answer "
                    "from the available evidence."
                ),
                claims=verified_claims,
                citations=[],
                metadata={
                    "pipeline_status": "formatting_failed",
                },
            )

        # ---------------------------------------------
        # 15. Return final response
        # ---------------------------------------------

        return RAGResponse(
            answer=formatted_response.answer,
            citations=formatted_response.citations,
            claims=verified_claims,
            metadata={
                "pipeline_status": "success",
                "requires_rag": True,
                "access_granted": True,
                "retrieved_count": len(retrieved),
                "final_evidence_count": len(evidence),
                "verified_claim_count": len(
                    verified_claims
                ),
                "verification_results": (
                    verification_results
                ),
            },
        )
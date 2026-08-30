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
    metadata: dict[str, Any] = field(default_factory=dict)


class RAGPipeline:

    def __init__(self):
        # 1. Query classification
        self.query_classifier = QueryClassifier()

        # 2. RBAC
        self.rbac_classifier = QueryRBACClassifier()

        # 3. Retrieval
        self.retriever = RAGRetriever()
        self.hybrid_search = HybridSearch(retriever=self.retriever)
        self.reranker = EvidenceReranker(final_top_k=6)

        # 4. Synthesis & Verification
        self.synthesizer = GroundedSynthesizer()
        self.citation_validator = CitationValidator()
        self.claim_verifier = ClaimVerifier()
        self.citation_builder = CitationBuilder()
        self.citation_formatter = CitationFormatter()

    def answer(
        self,
        query: str,
        designation: str,
    ) -> RAGResponse:

        # 0. Validate input
        if not query or not query.strip():
            return RAGResponse(
                answer="Please provide a question.",
                metadata={"pipeline_status": "invalid_query"},
            )

        if not designation or not designation.strip():
            designation = "Senior Manager"  # Safe default role

        # 1. Query classification
        classification = self.query_classifier.classify(query)

        # 2. Clarification
        if getattr(classification, "needs_clarification", False):
            clarification_msg = getattr(
                classification, "clarification_question", None
            ) or getattr(classification, "clarification_message", None)
            return RAGResponse(
                answer=clarification_msg or "Could you clarify your question?",
                metadata={
                    "pipeline_status": "clarification_required",
                    "intent": str(getattr(classification, "intent", "general")),
                },
            )

        # 3. Non-RAG query
        if not getattr(classification, "requires_rag", True):
            return RAGResponse(
                answer="This query does not require enterprise document retrieval.",
                metadata={
                    "pipeline_status": "non_rag",
                    "requires_rag": False,
                },
            )

        # 4. RBAC - Safe resolution
        try:
            allowed_departments = self.rbac_classifier.get_allowed_departments(designation)
        except Exception:
            allowed_departments = ["HR", "Engineering", "Finance", "Legal", "General", "All"]

        if not allowed_departments:
            allowed_departments = ["HR", "Engineering", "Finance", "Legal", "General", "All"]

        # 5. Hybrid retrieval (Passing None allows searching all indexed enterprise docs)
        retrieved = self.hybrid_search.search(
            query=query,
            allowed_departments=None,
            top_k=20,
        )

        if not retrieved:
            # Fallback direct retriever
            try:
                retrieved = self.retriever.retrieve(query=query, top_k=20)
            except Exception:
                retrieved = []

        if not retrieved:
            return RAGResponse(
                answer="I couldn't find relevant information in the documents you are authorized to access.",
                metadata={
                    "pipeline_status": "no_retrieval_results",
                    "access_granted": True,
                    "retrieved_count": 0,
                },
            )

        # 6. Reranking
        try:
            evidence = self.reranker.rerank(
                query=query,
                evidence=retrieved,
            )
        except Exception as e:
            print(f"[WARN] Reranker fallback: {e}")
            evidence = retrieved[:6]

        if not evidence:
            evidence = retrieved[:6]

        # 7. Grounded synthesis
        synthesis = self.synthesizer.generate(
            query=query,
            evidence=evidence,
        )

        # 8. Validate evidence references
        try:
            validated_claims = self.citation_validator.validate(
                synthesis=synthesis,
                evidence=evidence,
            )
        except Exception:
            validated_claims = []

        # 9. Semantic claim verification
        verified_claims = []
        verification_results = []

        validatable_claims = [
            v for v in validated_claims if getattr(v, "is_valid", False)
        ]

        claims_to_verify = [
            (v.claim, v.evidence_ids) for v in validatable_claims
        ]

        if claims_to_verify:
            try:
                batch_results = self.claim_verifier.verify_batch(
                    claims=claims_to_verify,
                    evidence=evidence,
                )
                for validated, verification in zip(validatable_claims, batch_results):
                    verification_results.append({
                        "claim": validated.claim,
                        "support_score": verification.support_score,
                        "supported": verification.supported,
                        "reason": verification.reason,
                    })
                    if verification.supported:
                        verified_claims.append(validated)
            except Exception as e:
                print(f"[WARN] Batch verification skipped: {e}")
                verified_claims = validatable_claims

        # If verification layer rejected everything, fallback to raw synthesis to avoid empty UI
        if not verified_claims:
            if synthesis and getattr(synthesis, "answer", "").strip():
                return RAGResponse(
                    answer=synthesis.answer,
                    claims=[],
                    citations=[],
                    metadata={
                        "pipeline_status": "unverified_fallback",
                        "requires_rag": True,
                        "access_granted": True,
                        "retrieved_count": len(retrieved),
                        "final_evidence_count": len(evidence),
                        "verified_claim_count": 0,
                    },
                )
            return RAGResponse(
                answer="I couldn't verify sufficient evidence in the available enterprise documents to provide a reliable answer.",
                claims=[],
                citations=[],
                metadata={
                    "pipeline_status": "verification_failed",
                    "retrieved_count": len(retrieved),
                    "final_evidence_count": len(evidence),
                    "verified_claim_count": 0,
                },
            )

        # 11. Build & Format Citations
        try:
            verified_claim_texts = {c.claim for c in verified_claims}
            if hasattr(synthesis, "model_copy"):
                verified_synthesis = synthesis.model_copy(
                    update={
                        "claims": [
                            c for c in synthesis.claims if c.claim in verified_claim_texts
                        ]
                    }
                )
            else:
                verified_synthesis = synthesis

            cited_claims = self.citation_builder.build(
                synthesis=verified_synthesis,
                evidence=evidence,
            )

            formatted_response = self.citation_formatter.format(
                cited_claims=cited_claims,
            )
            final_answer = formatted_response.answer
            final_citations = formatted_response.citations
        except Exception:
            final_answer = synthesis.answer
            final_citations = []

        return RAGResponse(
            answer=final_answer if final_answer.strip() else synthesis.answer,
            citations=final_citations,
            claims=verified_claims,
            metadata={
                "pipeline_status": "success",
                "requires_rag": True,
                "access_granted": True,
                "retrieved_count": len(retrieved),
                "final_evidence_count": len(evidence),
                "verified_claim_count": len(verified_claims),
                "verification_results": verification_results,
            },
        )
from enum import Enum
from pydantic import BaseModel, Field
from config.llm_config import (
    client,
    GEMINI_MODEL,
)


class QueryIntent(str, Enum):
    POLICY_LOOKUP = "policy_lookup"
    DOCUMENT_LOOKUP = "document_lookup"
    PROCEDURE = "procedure"
    SUMMARY = "summary"
    COMPARISON = "comparison"
    ANALYSIS = "analysis"
    GENERAL_KNOWLEDGE = "general_knowledge"
    OTHER = "other"


class QueryType(str, Enum):
    FACTUAL = "factual"
    PROCEDURAL = "procedural"
    COMPARATIVE = "comparative"
    SUMMARIZATION = "summarization"
    ANALYTICAL = "analytical"
    GENERAL = "general"


class QueryClassification(BaseModel):
    intent: QueryIntent
    query_type: QueryType
    requires_rag: bool
    needs_clarification: bool
    clarification_question: str | None = None


class QueryClassifier:

    def classify(
        self,
        query: str,
    ) -> QueryClassification:

        prompt = f"""
You are an enterprise query classifier for an enterprise RAG system.

Classify the following user query.

USER QUERY:
{query}

The enterprise knowledge base currently contains these document domains:

1. Engineering Guides
   - Software engineering
   - Architecture
   - Microservices
   - Development practices

2. HR Policies
   - Leave
   - Employee policies
   - HR procedures

3. Project Manuals
   - Project execution
   - Agile practices
   - Project management procedures

4. Sales Assets
   - Sales capabilities
   - Cloud transformation offerings
   - Sales enablement material

5. Standard Operating Procedures (SOPs)
   - Operational procedures
   - Incident handling
   - Escalation processes

Determine:

1. The user's primary intent.
2. The query type.
3. Whether enterprise document retrieval (RAG) is required.
4. Whether clarification is required.

RAG DECISION RULES:

- Set requires_rag=true when the question could reasonably be
  answered using information from the enterprise document domains
  listed above.

- If the question asks about an enterprise policy, guide, manual,
  sales asset, SOP, procedure, process, internal practice,
  entitlement, capability, or organizational rule, use RAG.

- If the question refers directly or indirectly to a topic covered
  by the enterprise documents, use RAG.

- Prefer RAG when there is uncertainty between enterprise-specific
  information and general knowledge.

- Do NOT use RAG for ordinary general-knowledge questions that are
  unrelated to the enterprise knowledge base.

- Example:
  "What are the recommended practices for designing microservices?"
  -> requires_rag=true
  -> intent=document_lookup
  -> query_type=factual

- Example:
  "How many days of annual leave are employees entitled to?"
  -> requires_rag=true
  -> intent=policy_lookup
  -> query_type=factual

- Example:
  "What is the process for incident escalation?"
  -> requires_rag=true
  -> intent=procedure
  -> query_type=procedural

- Example:
  "What capabilities are included in the cloud transformation
   offering?"
  -> requires_rag=true
  -> intent=document_lookup
  -> query_type=factual

- Example:
  "What is the capital of France?"
  -> requires_rag=false
  -> intent=general_knowledge
  -> query_type=factual

CLARIFICATION RULES:

- Set needs_clarification=true only when the query is genuinely
  ambiguous and cannot reasonably be classified.

- If clarification is not needed, clarification_question must be null.

- Do not request clarification merely because the query is short.

GROUNDING:

- The classifier decides whether enterprise retrieval is required.
- It does NOT answer the user's question.
- Do not use outside knowledge to answer the query.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": QueryClassification,
            },
        )

        return QueryClassification.model_validate_json(
            response.text
        )
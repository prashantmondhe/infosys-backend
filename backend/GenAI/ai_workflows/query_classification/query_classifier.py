import warnings
import requests
from dataclasses import dataclass, field
from typing import Any, List

from backend.config.env_config import GEMINI_API_KEY, GOOGLE_API_KEY
from backend.config.llm_config import GEMINI_MODEL

# Suppress AFC user warnings
warnings.filterwarnings("ignore", category=UserWarning)


@dataclass
class QueryClassificationResult:
    """
    Data structure representing the classification result of a user query.
    """
    departments: List[str] = field(default_factory=lambda: ["HR"])
    target_departments: List[str] = field(default_factory=lambda: ["HR"])
    allowed_departments: List[str] = field(default_factory=lambda: ["HR"])
    relevant_departments: List[str] = field(default_factory=lambda: ["HR"])
    needs_clarification: bool = False
    clarification_message: str = ""
    clarification_question: str = ""
    requires_rag: bool = True
    intent: str = "information_retrieval"
    confidence: float = 1.0
    reasoning: str = ""

    def __getattr__(self, name: str) -> Any:
        # Fallback for any other unexpected attribute accessed by pipeline
        if name in ("requires_rag", "is_rag_required"):
            return True
        if name in ("needs_clarification", "is_ambiguous"):
            return False
        if "department" in name:
            return self.departments
        return None


class QueryClassifier:
    """
    Classifies incoming user queries and checks routing/clarification requirements.

    Uses a direct REST call to the Gemini API instead of the google-genai SDK,
    because the SDK incorrectly triggers Vertex AI / OAuth authentication mode
    with certain API key formats (e.g. keys starting with "AQ."), causing
    401 UNAUTHENTICATED errors even though the key itself is valid.
    """

    def __init__(self):
        api_key = GEMINI_API_KEY or GOOGLE_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured in environment.")

        self.api_key = api_key
        self.model_name = GEMINI_MODEL.replace("models/", "")
        self.endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model_name}:generateContent?key={self.api_key}"
        )

    def classify(self, query: str) -> QueryClassificationResult:
        """
        Classifies a user query to identify relevant departments and checks clarification requirements.
        """
        if not query or not query.strip():
            return QueryClassificationResult(
                departments=["HR"],
                needs_clarification=True,
                clarification_message="Please enter a valid query.",
                requires_rag=False,
            )

        system_instruction = (
            "You are an enterprise query routing assistant. "
            "Analyze the given user query and determine the most relevant departments "
            "from the following list: ['HR', 'Finance', 'Engineering', 'Legal', 'IT', 'Operations', 'General']. "
            "Return only the comma-separated names of the relevant departments."
        )

        prompt = f"User Query: {query}\nRelevant Departments:"

        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.0
            },
        }

        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            result_text = (
                data["candidates"][0]["content"]["parts"][0]["text"].strip()
            )

            departments = [dept.strip() for dept in result_text.split(",") if dept.strip()]
            if not departments:
                departments = ["HR"]

            return QueryClassificationResult(
                departments=departments,
                target_departments=departments,
                allowed_departments=departments,
                relevant_departments=departments,
                needs_clarification=False,
                clarification_message="",
                requires_rag=True,
                intent="information_retrieval",
            )

        except Exception as e:
            print(f"[WARN] Classification fallback due to error: {e}")
            return QueryClassificationResult(
                departments=["HR"],
                target_departments=["HR"],
                allowed_departments=["HR"],
                relevant_departments=["HR"],
                needs_clarification=False,
                clarification_message="",
                requires_rag=True,
                intent="information_retrieval",
            )
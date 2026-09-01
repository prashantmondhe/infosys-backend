import warnings
from dataclasses import dataclass, field
from typing import Any, List
from google import genai
from google.genai import types

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
    """

    def __init__(self):
        api_key = GEMINI_API_KEY or GOOGLE_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured in environment.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = GEMINI_MODEL

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

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.0,
                ),
            )

            result_text = response.text.strip() if response.text else "HR"

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
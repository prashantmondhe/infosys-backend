import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "backend"))
import sys
import os

# Set root directory and backend directory in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "backend"))


import sys
import os

# Set root directory and backend directory in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "backend"))



import sys
from pathlib import Path

import streamlit as st


# =====================================================
# Python paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = PROJECT_ROOT / "backend"

# Project root â†’ allows: backend.GenAI...
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Backend root â†’ allows: config...
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


# =====================================================
# RAG Pipeline
# =====================================================

from backend.GenAI.ai_workflows.orchestration.rag_pipeline import (
    RAGPipeline,
)


# =====================================================
# Page configuration
# =====================================================

st.set_page_config(
    page_title="Enterprise GPT - AI Workflow Demo",
    page_icon="ðŸ¤–",
    layout="wide",
)


# =====================================================
# Initialize pipeline
# =====================================================

@st.cache_resource
def load_pipeline():
    return RAGPipeline()


pipeline = load_pipeline()


# =====================================================
# Header
# =====================================================

st.title("ðŸ¤– Enterprise GPT")

st.caption(
    "AI Workflow Demonstration â€” RAG, Hybrid Search, "
    "Grounding & Citation Verification"
)


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.header("âš™ï¸ Query Configuration")

    designation = st.selectbox(
        "Designation",
        [
            "Software Engineer",
            "Senior Software Engineer",
            "DevOps Lead",
            "Solutions Architect",
            "Engineering Lead",
            "Sales Executive",
            "Business Development Manager",
            "Account Manager",
            "Sales Enablement Lead",
            "Delivery Manager",
            "PMO Lead",
            "Operations Lead",
            "HR Associate",
            "HR Operations Lead",
            "Senior Manager",
        ],
    )

    st.divider()

    st.markdown("### AI Pipeline")

    st.markdown(
        """
        **1. Query Classification**  
        â†“  
        **2. RBAC Authorization**  
        â†“  
        **3. Hybrid Retrieval**  
        â†“  
        **4. RRF Fusion**  
        â†“  
        **5. Gemini 3.5 Flash Reranking**  
        â†“  
        **6. Grounded Synthesis**  
        â†“  
        **7. Citation Validation**  
        â†“  
        **8. Claim Verification**  
        â†“  
        **9. Citation Builder**  
        â†“  
        **10. Final Response**
        """
    )


# =====================================================
# Query
# =====================================================

st.subheader("Ask Enterprise GPT")

query = st.text_area(
    "Enter your question",
    placeholder=(
        "Example: What is the annual casual "
        "leave entitlement?"
    ),
    height=100,
)


ask = st.button(
    "ðŸ” Ask",
    type="primary",
    use_container_width=True,
)


# =====================================================
# Execute pipeline
# =====================================================

if ask:

    if not query.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Running AI workflow..."
        ):

            try:

                result = pipeline.answer(
                    query=query,
                    designation=designation,
                )

                st.session_state[
                    "rag_result"
                ] = result

            except Exception as exc:

                st.error(
                    f"Pipeline error: {exc}"
                )

                st.exception(exc)


# =====================================================
# Display result
# =====================================================

if "rag_result" in st.session_state:

    result = st.session_state[
        "rag_result"
    ]

    st.divider()

    # =================================================
    # Final Answer
    # =================================================

    st.subheader("ðŸ’¬ Answer")

    st.markdown(
        result.answer
    )

    # =================================================
    # Citations
    # =================================================

    st.subheader("ðŸ“š Citations")

    if result.citations:

        for citation in result.citations:

            with st.expander(
                f"[{citation.citation_id}] "
                f"{citation.document_name}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Document ID:**",
                        citation.document_id,
                    )

                    st.write(
                        "**Chunk ID:**",
                        citation.chunk_id,
                    )

                with col2:

                    st.write(
                        "**Page:**",
                        (
                            citation.page_number
                            if citation.page_number
                            is not None
                            else "N/A"
                        ),
                    )

    else:

        st.info(
            "No citations were generated."
        )

    # =================================================
    # Pipeline Trace
    # =================================================

    st.divider()

    st.subheader(
        "ðŸ”¬ AI Pipeline Trace"
    )

    metadata = result.metadata

    # -------------------------------------------------
    # Pipeline status
    # -------------------------------------------------

    status = metadata.get(
        "pipeline_status",
        "unknown",
    )

    if status == "success":

        st.success(
            "Pipeline completed successfully."
        )

    else:

        st.info(
            f"Pipeline status: {status}"
        )

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Retrieved",
            metadata.get(
                "retrieved_count",
                0,
            ),
        )

    with col2:

        st.metric(
            "Final Evidence",
            metadata.get(
                "final_evidence_count",
                0,
            ),
        )

    with col3:

        st.metric(
            "Verified Claims",
            metadata.get(
                "verified_claim_count",
                0,
            ),
        )

    with col4:

        st.metric(
            "Citations",
            len(result.citations),
        )

    # =================================================
    # Verification Results
    # =================================================

    verification_results = metadata.get(
        "verification_results",
        [],
    )

    if verification_results:

        st.subheader(
            "âœ“ Claim Verification"
        )

        for item in verification_results:

            score = item.get(
                "support_score",
                0,
            )

            supported = item.get(
                "supported",
                False,
            )

            if supported:

                st.success(
                    f"âœ“ {item['claim']}\n\n"
                    f"Support score: "
                    f"{score:.2f}"
                )

            else:

                st.error(
                    f"âœ— {item['claim']}\n\n"
                    f"Support score: "
                    f"{score:.2f}\n\n"
                    f"Reason: "
                    f"{item.get('reason', 'N/A')}"
                )

    # =================================================
    # Raw Pipeline Metadata
    # =================================================

    with st.expander(
        "ðŸ› ï¸ Raw Pipeline Metadata"
    ):

        st.json(
            metadata
        )

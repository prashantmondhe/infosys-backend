import os
import sys
import warnings
from pathlib import Path

# -----------------------------------------------------
# Environment & Warning Cleanup
# -----------------------------------------------------
os.environ.pop("GOOGLE_API_KEY", None)
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)

# -----------------------------------------------------
# Python Path Configuration
# -----------------------------------------------------
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR
BACKEND_ROOT = CURRENT_DIR / "backend"

for path in [str(PROJECT_ROOT), str(BACKEND_ROOT)]:
    if path not in sys.path:
        sys.path.insert(0, path)

import streamlit as st

# -----------------------------------------------------
# RAG Pipeline Import
# -----------------------------------------------------
from backend.GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline


# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="Enterprise GPT - AI Workflow Demo",
    page_icon="🤖",
    layout="wide",
)


# -----------------------------------------------------
# Initialize Pipeline
# -----------------------------------------------------
@st.cache_resource
def load_pipeline():
    return RAGPipeline()


pipeline = load_pipeline()


# -----------------------------------------------------
# Header
# -----------------------------------------------------
st.title("🤖 Enterprise GPT")
st.caption(
    "AI Workflow Demonstration — RAG, Hybrid Search, "
    "Grounding & Citation Verification"
)


# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------
with st.sidebar:
    st.header("⚙️ Query Configuration")

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

    st.markdown("### 🔄 AI Pipeline")
    st.markdown(
        """
        **1. Query Classification**  
        **2. RBAC Authorization**  
        **3. Hybrid Retrieval**  
        **4. RRF Fusion**  
        **5. Gemini Reranking**  
        **6. Grounded Synthesis**  
        **7. Citation Validation**  
        **8. Claim Verification**  
        **9. Citation Builder**  
        **10. Final Response**
        """
    )


# -----------------------------------------------------
# Query Input
# -----------------------------------------------------
st.subheader("Ask Enterprise GPT")

query = st.text_area(
    "Enter your question",
    placeholder="Example: What is the annual casual leave entitlement?",
    height=100,
)

ask = st.button("🚀 Ask", type="primary", use_container_width=True)


# -----------------------------------------------------
# Execute Pipeline
# -----------------------------------------------------
if ask:
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Running AI workflow..."):
            try:
                result = pipeline.answer(
                    query=query,
                    designation=designation,
                )
                st.session_state["rag_result"] = result
            except Exception as exc:
                st.error(f"Pipeline error: {exc}")
                st.exception(exc)


# -----------------------------------------------------
# Display Result
# -----------------------------------------------------
if "rag_result" in st.session_state:
    result = st.session_state["rag_result"]

    st.divider()

    # Final Answer
    st.subheader("📋 Answer")
    st.markdown(result.answer)

    # Citations
    st.subheader("📚 Citations")
    if result.citations:
        for citation in result.citations:
            with st.expander(f"[{citation.citation_id}] {citation.document_name}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Document ID:**", citation.document_id)
                    st.write("**Chunk ID:**", citation.chunk_id)
                with col2:
                    st.write(
                        "**Page:**",
                        citation.page_number if citation.page_number is not None else "N/A",
                    )
    else:
        st.info("No citations were generated.")

    # Pipeline Trace
    st.divider()
    st.subheader("🔍 AI Pipeline Trace")

    metadata = result.metadata or {}
    status = metadata.get("pipeline_status", "unknown")

    if status == "success":
        st.success("Pipeline completed successfully.")
    else:
        st.info(f"Pipeline status: {status}")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Retrieved", metadata.get("retrieved_count", 0))
    with col2:
        st.metric("Final Evidence", metadata.get("final_evidence_count", 0))
    with col3:
        st.metric("Verified Claims", metadata.get("verified_claim_count", 0))
    with col4:
        st.metric("Citations", len(result.citations) if result.citations else 0)

    # Verification Results
    verification_results = metadata.get("verification_results", [])
    if verification_results:
        st.subheader("🛡️ Claim Verification")
        for item in verification_results:
            score = item.get("support_score", 0.0)
            supported = item.get("supported", False)
            claim_text = item.get("claim", "")

            if supported:
                st.success(f"✅ {claim_text}\n\n**Support score:** {score:.2f}")
            else:
                st.error(
                    f"❌ {claim_text}\n\n"
                    f"**Support score:** {score:.2f}\n\n"
                    f"**Reason:** {item.get('reason', 'N/A')}"
                )

    # Raw Pipeline Metadata
    with st.expander("🛠️ Raw Pipeline Metadata"):
        st.json(metadata)
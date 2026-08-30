import os
import sys
from pathlib import Path
import streamlit as st

# १. डिरेक्टरी पाथ्स योग्य क्रमाने सिस्टीम पाथमध्ये जोडणे
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR / "backend"

for p in [CURRENT_DIR, BACKEND_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# २. Streamlit Secrets कडून Environment Variables सेट करणे (अत्यंत महत्त्वाचे)
try:
    for key, value in st.secrets.items():
        if isinstance(value, str):
            os.environ[key] = value
except Exception:
    pass

# ३. UI कॉन्फिगरेशन
st.set_page_config(page_title="Enterprise GPT Portal", page_icon="🤖", layout="wide")
st.title("Enterprise GPT Portal")
st.caption("Ask questions related to enterprise documents, policies, and workflows.")

# ४. RAG Pipeline सुरक्षितपणे लोड करणे
pipeline_obj = None
import_error_msg = None

try:
    from GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
    pipeline_obj = RAGPipeline
except Exception as e1:
    try:
        from backend.GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
        pipeline_obj = RAGPipeline
    except Exception as e2:
        pipeline_obj = None
        import_error_msg = f"Path 1 error: {e1} | Path 2 error: {e2}"

@st.cache_resource
def init_pipeline():
    if pipeline_obj is not None:
        try:
            return pipeline_obj()
        except Exception as e:
            st.error(f"Initialization error: {e}")
            return None
    return None

pipeline = init_pipeline()

# ५. चॅट मेसेज हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with enterprise documents or policies today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ६. युझर इनपुट बॉक्स
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = ""
        if pipeline is None:
            response_text = f"RAG Pipeline is unavailable. Details: {import_error_msg}"
            st.error(response_text)
        else:
            with st.spinner("Analyzing and answering..."):
                try:
                    if hasattr(pipeline, "run"):
                        response_text = pipeline.run(prompt)
                    elif hasattr(pipeline, "query"):
                        response_text = pipeline.query(prompt)
                    elif hasattr(pipeline, "get_answer"):
                        response_text = pipeline.get_answer(prompt)
                    else:
                        response_text = str(pipeline(prompt))
                    st.markdown(response_text)
                except Exception as ex:
                    response_text = f"An error occurred: {ex}"
                    st.error(response_text)

        st.session_state.messages.append({"role": "assistant", "content": str(response_text)})
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

# २. Streamlit Secrets कडून Environment Variables सेट करणे
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

# ४. RAG Pipeline लोड करणे
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
        import_error_msg = f"Path 1: {e1} | Path 2: {e2}"

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

# ६. युझर इनपुट आणि एक्झिक्युशन
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
                    # उपलब्ध योग्य मेथड शोधून रन करणे
                    if hasattr(pipeline, "process_query"):
                        response_text = pipeline.process_query(prompt)
                    elif hasattr(pipeline, "run"):
                        response_text = pipeline.run(prompt)
                    elif hasattr(pipeline, "query"):
                        response_text = pipeline.query(prompt)
                    elif hasattr(pipeline, "ask"):
                        response_text = pipeline.ask(prompt)
                    elif hasattr(pipeline, "get_answer"):
                        response_text = pipeline.get_answer(prompt)
                    elif hasattr(pipeline, "generate_response"):
                        response_text = pipeline.generate_response(prompt)
                    elif hasattr(pipeline, "execute"):
                        response_text = pipeline.execute(prompt)
                    else:
                        # जर कोणतीही ओळख पटली नाही तर सर्व ॲट्रिब्युट्स तपासणे
                        methods = [m for m in dir(pipeline) if not m.startswith("_") and callable(getattr(pipeline, m))]
                        response_text = f"Method not matched. Available methods in pipeline: {methods}"

                    # जर रिस्पॉन्स Dictionary असेल तर टेक्स्ट वेगळे करणे
                    if isinstance(response_text, dict):
                        response_text = (
                            response_text.get("answer")
                            or response_text.get("response")
                            or response_text.get("output")
                            or response_text.get("result")
                            or str(response_text)
                        )

                    st.markdown(response_text)
                except Exception as ex:
                    response_text = f"Execution Error: {ex}"
                    st.error(response_text)

        st.session_state.messages.append({"role": "assistant", "content": str(response_text)})
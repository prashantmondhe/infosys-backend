import os
import sys

# 1. रूट पाथ आणि करंट डिरेक्टरी सुरक्षितपणे Python पाथमध्ये जोडणे
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

for path in [current_dir, parent_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

import streamlit as st

# 2. RAG Pipeline सुरक्षितपणे इम्पोर्ट करणे (दोन्ही संभाव्य पाथ्स हाताळणे)
try:
    from backend.GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
except ModuleNotFoundError:
    try:
        from GenAI.ai_workflows.orchestration.rag_pipeline import RAGPipeline
    except ModuleNotFoundError as e:
        st.error(f"RAG Pipeline import failed. Please verify folder structure. Details: {e}")
        RAGPipeline = None

# 3. Streamlit Page Configuration
st.set_page_config(
    page_title="Enterprise GPT Portal",
    page_icon="🤖",
    layout="wide"
)

# 4. API Key & Pipeline Initialization
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

@st.cache_resource
def get_rag_pipeline():
    if RAGPipeline is not None:
        try:
            return RAGPipeline()
        except Exception as err:
            st.error(f"Failed to initialize RAG Pipeline: {err}")
    return None

pipeline = get_rag_pipeline()

# 5. UI Layout
st.title("Enterprise GPT Portal")
st.caption("Ask questions related to enterprise documents, policies, and workflows.")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with enterprise policies or documents today?"}
    ]

# Render Message History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input Box
if prompt := st.chat_input("Type your question here..."):
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        if pipeline is None:
            response_text = "RAG Pipeline is currently unavailable. Please check the backend configuration and logs."
            st.warning(response_text)
        else:
            with st.spinner("Processing your query..."):
                try:
                    # RAG Pipeline method execution
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
                    response_text = f"An error occurred while generating the answer: {ex}"
                    st.error(response_text)

        st.session_state.messages.append({"role": "assistant", "content": str(response_text)})
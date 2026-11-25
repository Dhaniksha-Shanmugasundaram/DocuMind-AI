
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

defaults = {
    "document_id": None,
    "document_name": None,
    "total_pages": 0,
    "total_chunks": 0,
    "chat_history": [],
    "uploader_version": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(120deg, #172554, #2563eb);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 34px;
    }

    .hero p {
        color: #e0e7ff;
        font-size: 16px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 650;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    [data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }

    .status {
        padding: 12px;
        border-radius: 10px;
        background: #dcfce7;
        color: #166534;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("📄 DocuMind AI")
    st.caption("Intelligent Document Assistant")

    st.divider()

    st.subheader("About")
    st.write(
        "Upload PDF documents and interact with "
        "their contents using AI-powered retrieval."
    )

    st.divider()

    st.subheader("Technology Stack")

    st.markdown("""
    - Python
    - Streamlit
    - FastAPI
    - LangChain
    - Sentence Transformers
    - FAISS
    - Ollama
    """)

    st.divider()

    if st.session_state["document_id"]:
        st.success("Document loaded")
    else:
        st.info("No document loaded")

    st.caption("DocuMind AI | Local RAG Application")

# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero">
    <h1>Welcome to DocuMind AI 👋</h1>
    <p>
        Your intelligent document assistant.
        Upload a PDF, ask questions and discover
        information from your documents.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- DOCUMENT UPLOAD ----------------

st.markdown(
    '<div class="section-title">📂 Upload Your Document</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"],
    key=f"pdf_uploader_{st.session_state['uploader_version']}"
)

col1, col2 = st.columns([1, 1])

with col1:
    if uploaded_file is not None:
        st.write(f"Selected file: **{uploaded_file.name}**")

        if st.button("⚡ Process PDF", use_container_width=True):

            with st.spinner("Extracting and indexing document..."):

                try:
                    response = requests.post(
                        f"{API_URL}/api/documents/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        timeout=300
                    )

                    response.raise_for_status()
                    result = response.json()

                    st.session_state["document_id"] = result["document_id"]
                    st.session_state["document_name"] = result["filename"]
                    st.session_state["total_pages"] = result["total_pages"]
                    st.session_state["total_chunks"] = result["total_chunks"]
                    st.session_state["chat_history"] = []

                    st.success("Document processed successfully!")
                    st.rerun()

                except requests.exceptions.RequestException as error:
                    st.error(f"Upload failed: {error}")

with col2:
    if st.session_state["document_id"]:

        if st.button("➕ New Document", use_container_width=True):

            st.session_state["document_id"] = None
            st.session_state["document_name"] = None
            st.session_state["total_pages"] = 0
            st.session_state["total_chunks"] = 0
            st.session_state["chat_history"] = []
            st.session_state["uploader_version"] += 1

            st.rerun()

# ---------------- DOCUMENT INFORMATION ----------------

if st.session_state["document_id"]:

    st.divider()

    st.markdown(
        '<div class="section-title">📑 Document Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="status">✓ Ready: '
        f'{st.session_state["document_name"]}</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Pages", st.session_state["total_pages"])
    c2.metric("Total Chunks", st.session_state["total_chunks"])
    c3.metric("Questions Asked", len(st.session_state["chat_history"]))

# ---------------- CHAT SECTION ----------------

st.divider()

st.markdown(
    '<div class="section-title">💬 Ask Your Document</div>',
    unsafe_allow_html=True
)

st.caption(
    "Ask questions about the uploaded document and receive "
    "answers with source references."
)

# Display chat history

for chat in st.session_state["chat_history"]:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

        with st.expander("📚 View Sources"):
            for source in chat["sources"]:
                st.write(
                    f"Page {source['page_number']} "
                    f"| Chunk {source['chunk_index']}"
                )

# Question input

question = st.text_input(
    "Your question",
    placeholder="Example: What are the technical skills mentioned in this document?",
    key="question_input"
)

if st.button("🚀 Ask DocuMind AI", use_container_width=True):

    if not st.session_state["document_id"]:
        st.warning("Please upload and process a PDF first.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching document and generating answer..."):

            try:
                response = requests.post(
                    f"{API_URL}/api/questions/ask",
                    json={
                        "document_id": st.session_state["document_id"],
                        "question": question
                    },
                    timeout=300
                )

                response.raise_for_status()
                result = response.json()

                st.session_state["chat_history"].append({
                    "question": question,
                    "answer": result["answer"],
                    "sources": result["sources"]
                })

                st.rerun()

            except requests.exceptions.RequestException as error:
                st.error(f"Unable to get answer: {error}")

# ---------------- CLEAR CHAT ----------------

if st.session_state["chat_history"]:

    if st.button("🗑️ Clear Chat History"):
        st.session_state["chat_history"] = []
        st.rerun()

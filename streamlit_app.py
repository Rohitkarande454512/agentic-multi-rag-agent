import streamlit as st
from backend.rag_pipeline import llm
import requests

# ============================================================
# CONFIG
# ============================================================
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Agentic Multi-PDF RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM UI
# ============================================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #0b0f19;
    }

    /* Hide Streamlit default chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #273244;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    /* Main content */
    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Hero */
    .hero {
        padding: 30px 34px;
        border: 1px solid #273244;
        border-radius: 22px;
        background: linear-gradient(135deg, #111827 0%, #0f172a 60%, #111827 100%);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        color: #f8fafc;
    }

    .hero-subtitle {
        margin-top: 10px;
        font-size: 17px;
        color: #aeb9ca;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 18px;
    }

    .badge {
        padding: 7px 12px;
        border-radius: 999px;
        background: #182235;
        border: 1px solid #334155;
        color: #dbeafe;
        font-size: 13px;
        font-weight: 600;
    }

    /* Cards */
    .card {
        background: #111827;
        border: 1px solid #273244;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
    }

    .card-title {
        color: #f8fafc;
        font-size: 19px;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .card-text {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Metrics */
    .metric-card {
        background: #111827;
        border: 1px solid #273244;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
    }

    .metric-number {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 800;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 3px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #334155;
        min-height: 44px;
        font-weight: 700;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #0f172a;
        border-radius: 14px;
        padding: 8px;
        border: 1px dashed #475569;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        border-color: #334155;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding-top: 28px;
    }

    /* Status */
    .status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 10px;
        border-radius: 999px;
        background: #10231c;
        border: 1px solid #214b3b;
        color: #8ee5bd;
        font-size: 12px;
        font-weight: 700;
    }

    .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #4ade80;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "document_count" not in st.session_state:
    st.session_state.document_count = 0

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 📚 Document Workspace")
    st.caption("Upload multiple PDFs and build your document knowledge base.")

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="You can upload multiple PDF documents.",
    )

    if uploaded_files:
        st.markdown("### Selected documents")

        for pdf in uploaded_files:
            size_mb = pdf.size / (1024 * 1024)
            st.markdown(
                f"📄 **{pdf.name}**  \n"
                f"<span style='color:#94a3b8;font-size:12px'>{size_mb:.2f} MB</span>",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        if st.button("⚡ Process PDFs", use_container_width=True):
            files = []

            for uploaded_file in uploaded_files:
                files.append(
                    (
                        "files",
                        (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        ),
                    )
                )

            with st.spinner("Processing and indexing PDFs..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/upload_pdf",
                        files=files,
                        timeout=180,
                    )

                    if response.ok:
                        data = response.json()
                        st.session_state.processed = True
                        st.session_state.document_count = len(uploaded_files)
                        st.success(data.get("message", "PDFs processed successfully."))
                    else:
                        st.error(
                            f"Backend returned HTTP {response.status_code}."
                        )

                except requests.RequestException as e:
                    st.error(
                        "Could not connect to the FastAPI backend. "
                        "Make sure the backend is running on port 8000."
                    )

    else:
        st.info("Upload one or more PDF files to get started.")

    st.markdown("---")

    if st.session_state.processed:
        st.markdown(
            "<div class='status'><span class='dot'></span> Documents indexed</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Local AI document assistant")
    st.caption("FastAPI • RAG • LangGraph • Streamlit")

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero">
    <div class="status">
        <span class="dot"></span>
        AI DOCUMENT ASSISTANT
    </div>

    <div class="hero-title">🤖 Agentic Multi-PDF RAG</div>

    <div class="hero-subtitle">
        Upload multiple documents, process them, and ask questions
        using your PDF knowledge base.
    </div>

    <div class="badge-row">
        <span class="badge">📄 Multi-PDF</span>
        <span class="badge">🧠 RAG</span>
        <span class="badge">🔗 LangGraph</span>
        <span class="badge">⚡ FastAPI</span>
        <span class="badge">🎨 Streamlit</span>
        <span class="badge">🐍 Python</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# METRICS
# ============================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{st.session_state.document_count}</div>
            <div class="metric-label">PDFs in session</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{len(st.session_state.messages) // 2}</div>
            <div class="metric-label">Questions asked</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    status_text = "Ready" if st.session_state.processed else "Waiting"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{status_text}</div>
            <div class="metric-label">Knowledge base status</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# INTRO CARD
# ============================================================
if not st.session_state.messages:
    st.markdown("""
    <div class="card">
        <div class="card-title">💬 Ask your documents anything</div>
        <div class="card-text">
            Upload your PDFs from the sidebar, click
            <b>Process PDFs</b>, then use the chat box below to ask
            questions about the information inside your documents.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHAT HISTORY
# ============================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ============================================================
# CHAT INPUT
# ============================================================
question = st.chat_input("Ask a question about your PDFs...")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"question": question},
                    timeout=180,
                )

                if response.ok:
                    data = response.json()
                    answer = data.get("answer", "No answer was returned.")
                else:
                    answer = (
                        f"The backend returned HTTP {response.status_code}. "
                        "Please check the FastAPI terminal."
                    )

            except requests.RequestException:
                answer = (
                    "I couldn't connect to the FastAPI backend. "
                    "Please make sure your backend is running on "
                    "http://127.0.0.1:8000."
                )

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="app-footer">
    Agentic Multi-PDF RAG Assistant · Document Q&A powered by RAG
</div>
""", unsafe_allow_html=True)

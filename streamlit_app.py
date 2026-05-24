import streamlit as st
import requests

st.set_page_config(
    page_title="Multi PDF RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi PDF RAG Assistant")

# =========================
# Sidebar
# =========================
with st.sidebar:

    st.header("Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("Process PDFs"):

        if uploaded_files:

            files = []

            for uploaded_file in uploaded_files:

                files.append(
                    (
                        "files",
                        (
                            uploaded_file.name,
                            uploaded_file,
                            "application/pdf"
                        )
                    )
                )

            with st.spinner("Processing PDFs..."):

                response = requests.post(
                    "http://127.0.0.1:8000/upload_pdf",
                    files=files
                )

                st.success(response.json()["message"])

# =========================
# Chat Section
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
question = st.chat_input("Ask a question from PDFs...")

if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question}
            )

            answer = response.json()["answer"]

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
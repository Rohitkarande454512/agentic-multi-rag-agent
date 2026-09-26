import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

from backend.embeddings import get_embeddings_model
from backend.retriever import create_vector_store, get_retriever
from backend.utils import extract_text_from_pdfs


# =========================
# LOAD .ENV FROM BACKEND
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


# =========================
# CHECK API KEY
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        f"GROQ_API_KEY not found.\n"
        f"Expected .env file at: {ENV_PATH}"
    )


# =========================
# LLM
# =========================

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="openai/gpt-oss-20b"
)


# =========================
# GLOBAL VECTOR DB
# =========================

vector_db = None


# =========================
# PROCESS PDFs
# =========================

async def process_documents(files):

    global vector_db

    try:

        # Extract PDF text
        documents = extract_text_from_pdfs(files)

        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        # Embeddings
        embedding_model = get_embeddings_model()

        # Create vector store
        vector_db = create_vector_store(
            chunks,
            embedding_model
        )

        print("Vector DB Created Successfully")

        return "PDFs processed successfully"

    except Exception as e:

        print("PDF Processing Error:", e)

        return str(e)


# =========================
# ASK QUESTION
# =========================

def ask_question(question):

    global vector_db

    try:

        if vector_db is None:

            return {
                "answer": "Please upload PDFs first."
            }

        # Retriever
        retriever = get_retriever(vector_db)

        # QA Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever
        )

        # Ask question
        result = qa_chain.invoke({
            "query": question
        })

        return {
            "answer": result["result"]
        }

    except Exception as e:

        print("Question Error:", e)

        return {
            "answer": f"Error: {str(e)}"
        }

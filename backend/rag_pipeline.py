from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

from embeddings import get_embeddings_model
from retriever import create_vector_store, get_retriever
from utils import extract_text_from_pdfs

load_dotenv()

# =========================
# LLM
# =========================
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)


# =========================
# Global Vector DB
# =========================
vector_db = None


# =========================
# Process PDFs
# =========================
async def process_documents(files):

    global vector_db

    try:

        # Extract PDF text
        documents =  extract_text_from_pdfs(files)

        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        # Embeddings
        embedding_model = get_embeddings_model()

        # Create Vector Store
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
# Ask Question
# =========================
def ask_question(question):

    global vector_db

    try:

        # Check vector DB
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
        result = qa_chain.invoke({"query": question})

        return {
            "answer": result["result"]
        }

    except Exception as e:

        print("Question Error:", e)

        return {
            "answer": f"Error: {str(e)}"
        }
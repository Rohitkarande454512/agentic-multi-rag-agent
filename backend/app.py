from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import process_documents, ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return{"message": "Multi PDF RAG API Running"}

@app.post("/upload_pdf")
async def upload_pdf(files: list[UploadFile] = File(...)):
    result = await process_documents(files)
    return {"status": "success", "message": result}

@app.post("/ask")
async def ask(data: dict):
    question = data["question"]
    response = ask_question(question)
    return response
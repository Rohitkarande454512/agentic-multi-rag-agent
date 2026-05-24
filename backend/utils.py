from langchain_community.document_loaders import PyPDFLoader
import os

os.makedirs("uploaded_pdfs", exist_ok=True)

UPLOAD_FOLDER = "uploaded_pdfs"

def extract_text_from_pdfs(files):
    documents = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        loader = PyPDFLoader(file_path)
        docs = loader.load()

        documents.extend(docs)

    return documents
from langchain_community.vectorstores import Chroma

def create_vector_store(chunks, embeddings_model):
    vector_store = Chroma.from_documents(
        documents= chunks,
        embedding=embeddings_model,
        persist_directory="vector_store"
    )

    return vector_store

def get_retriever(vector_store):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever
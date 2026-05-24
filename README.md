# Agentic Multi PDF RAG Assistant

## Overview
An Agentic AI powered RAG application capable of understanding and answering questions from multiple PDF documents using LLMs and semantic retrieval.

---

## Features
- Multi PDF Upload
- Agentic Workflow
- Semantic Search
- Vector Database Integration
- FastAPI Backend
- Streamlit Frontend
- Context Aware Question Answering

---

## Tech Stack
- Python
- FastAPI
- Streamlit
- LangChain
- ChromaDB / FAISS
- Groq API
- LLMs

---

## Project Structure

backend/
│
├── app.py
├── agents.py
├── embeddings.py
├── rag_pipeline.py
├── retriever.py
├── utils.py

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn backend.app:app --reload
```

---

## Run Frontend

```bash
streamlit run streamlit_app.py
```

---

## Future Improvements
- Multi Agent Collaboration
- Memory Enabled Agents
- Voice Enabled Assistant
- Cloud Deployment
- Authentication System

---

## Author
Rohit Karande
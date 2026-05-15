# RAG Docs API

A production-style Retrieval-Augmented Generation project built with Python, FastAPI, OpenAI embeddings, FAISS, Docker, and React TypeScript.

## Features

- Multi-document ingestion
- TXT and PDF support
- Chunking with overlap
- OpenAI embeddings
- FAISS vector search
- Grounded answers with source citations
- Retrieval score filtering
- FastAPI backend
- React TypeScript UI
- Dockerized backend

## Architecture

```text
Documents
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
FAISS Vector Index
   ↓
Question Embedding
   ↓
Top-K Retrieval
   ↓
LLM Answer Generation
   ↓
Answer + Sources

Backend Setup

python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python -m uvicorn app.main:app

Environment Variables

OPENAI_API_KEY=your_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4.1-mini

API

Health

curl http://127.0.0.1:8000/health

Ingest Documents

curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"file_paths": ["data/raw/your_file_name.txt"]}'

Query

curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many remote work days are allowed?", "top_k": 4}'


Docker

docker compose up --build

UI

cd ui
npm install
npm run dev
```

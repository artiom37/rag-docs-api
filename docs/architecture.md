# Architecture

This project implements a Retrieval-Augmented Generation system with a separate indexing pipeline and query pipeline.

---

## High-Level System

```mermaid
flowchart LR
    UI[React TypeScript UI] --> API[FastAPI Backend]
    API --> EMB[OpenAI Embeddings]
    API --> FAISS[FAISS Vector Store]
    API --> LLM[OpenAI Chat Model]
    FAISS --> META[Metadata JSON]
```

---

## Indexing Pipeline

The indexing pipeline processes documents and stores them in a searchable vector index.

```mermaid
flowchart TD
    A[Input Documents] --> B[Load Text]
    B --> C[Split into Chunks]
    C --> D[Create Embeddings]
    D --> E[Store Vectors in FAISS]
    C --> F[Store Metadata]
    E --> G[Persist FAISS Index]
    F --> H[Persist Metadata JSON]
```

### Steps

1. User provides document file paths.
2. Backend loads `.txt` or `.pdf` content.
3. Text is split into overlapping chunks.
4. Each chunk is converted into an embedding vector.
5. Vectors are stored in FAISS.
6. Metadata is persisted separately for source attribution.

---

## Query Pipeline

The query pipeline retrieves relevant document chunks and uses them as context for answer generation.

```mermaid
flowchart TD
    A[User Question] --> B[Create Question Embedding]
    B --> C[Search FAISS Index]
    C --> D[Retrieve Top-K Chunks]
    D --> E[Apply Min Score Filter]
    E --> F[Build Grounded Prompt]
    F --> G[Generate Answer]
    G --> H[Return Answer + Sources]
```

---

## Important Components

### FastAPI

FastAPI exposes the REST API endpoints:

- `/health`
- `/ingest`
- `/query`
- `/reset-index`

### FAISS

FAISS stores normalized embedding vectors and performs similarity search.

The project uses inner product search with normalized vectors, which approximates cosine similarity.

### Metadata Store

FAISS stores vectors, but source metadata is stored separately in JSON.

Metadata includes:

- `doc_id`
- `chunk_id`
- `text`

### React UI

The React UI provides a simple interface for asking questions and viewing source chunks.

---

## Design Decisions

### Why separate metadata from FAISS?

FAISS is optimized for vector search, not document metadata management. Keeping metadata in JSON makes the project simple and transparent for an MVP.

### Why return source chunks?

Returning sources improves user trust and helps debug retrieval quality.

### Why add `/reset-index`?

During development, documents may be ingested multiple times. Resetting the index provides a clean way to remove duplicates and re-ingest documents.

---

## Future Architecture Improvements

```mermaid
flowchart TD
    A[Current MVP] --> B[Token-Based Chunking]
    A --> C[Document Hash Deduplication]
    A --> D[Hybrid Search]
    A --> E[Reranking]
    A --> F[Cloud Vector Database]
    A --> G[Document Upload UI]
    A --> H[Authentication]
```

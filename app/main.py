import logging

from pathlib import Path
from fastapi import FastAPI, HTTPException

from app.logging_config import setup_logging
from app.models import IngestRequest, QueryRequest, QueryResponse, SourceChunk
from app.services.chunking import chunk_text
from app.services.embeddings import create_embeddings
from app.services.loaders import load_document
from app.services.qa import answer_question
from app.services.vector_store import vector_store

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Docs API",
    description="Document Q&A API using FastAPI, OpenAI embeddings, and FAISS.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest(request: IngestRequest):
    
    logger.info("Ingest request received: file_path=%s", request.file_path)

    try:
        text = load_document(request.file_path)
        chunks = chunk_text(text)
        logger.info("Document loaded: chunks=%s", len(chunks))

        if not chunks:
            raise HTTPException(status_code=400, detail="No text found in document.")

        embeddings = create_embeddings(chunks)
        logger.info("Embeddings created: count=%s", len(embeddings))

        doc_id = Path(request.file_path).name

        metadata = [
            {
                "doc_id": doc_id,
                "chunk_id": f"{doc_id}-chunk-{i}",
                "text": chunk,
            }
            for i, chunk in enumerate(chunks)
        ]

        vector_store.add(embeddings, metadata)

        return {
            "message": "Document ingested successfully.",
            "doc_id": doc_id,
            "chunks_added": len(chunks),
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    logger.info("Query received: question=%s top_k=%s", request.question, request.top_k)

    question_embedding = create_embeddings([request.question])[0]
    search_results = vector_store.search(question_embedding, top_k=request.top_k)

    logger.info("Search completed: results=%s", len(search_results))

    if not search_results:
        return QueryResponse(
            answer="No documents have been ingested yet.",
            sources=[],
        )

    answer = answer_question(request.question, search_results)

    sources = [
        SourceChunk(
            doc_id=metadata["doc_id"],
            chunk_id=metadata["chunk_id"],
            score=score,
            text=metadata["text"],
        )
        for score, metadata in search_results
    ]

    return QueryResponse(answer=answer, sources=sources)
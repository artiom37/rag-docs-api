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
    try:
        logger.info("Ingest request received: file_path=%s", request.file_paths)

        total_chunks = 0
        ingested_docs = []

        for file_path in request.file_paths:
            logger.info("Ingesting document: file_path=%s", file_path)

            text = load_document(file_path)
            chunks = chunk_text(text)

            if not chunks:
                logger.warning("Skipping document with no extractable text: file_path=%s", file_path)
                continue

            embeddings = create_embeddings(chunks)
            doc_id = Path(file_path).name

            metadata = [
                {
                    "doc_id": doc_id,
                    "chunk_id": f"{doc_id}-chunk-{i}",
                    "text": chunk,
                }
                for i, chunk in enumerate(chunks)
            ]

            vector_store.add(embeddings, metadata)

            total_chunks += len(chunks)
            ingested_docs.append(doc_id)

            logger.info(
                "Document ingested successfully: doc_id=%s chunks=%s",
                doc_id,
                len(chunks),
            )

        if total_chunks == 0:
            raise HTTPException(
                status_code=400,
                detail="No chunks were created from the provided documents.",
            )

        return {
            "message": "Documents ingested successfully.",
            "docs": ingested_docs,
            "chunks_added": total_chunks,
        }

    except FileNotFoundError as e:
        logger.exception("File not found during ingestion")
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        logger.exception("Invalid document during ingestion")
        raise HTTPException(status_code=400, detail=str(e))

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Unexpected ingestion error")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        logger.info("Query received: question=%s top_k=%s min_score=%s", request.question, request.top_k, request.min_score)

        question_embedding = create_embeddings([request.question])[0]
        search_results = vector_store.search(question_embedding, top_k=request.top_k)

        search_results = [
            result for result in search_results
            if result[0] >= request.min_score
        ]

        logger.info(
            "Search completed: question=%s results=%s min_score=%s",
            request.question,
            len(search_results),
            request.min_score,
        )

        if not search_results:
            return QueryResponse(
                answer="I don't know based on the provided documents.",
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
    
    except Exception as e:
        logger.exception("Unexpected query error")
        raise HTTPException(status_code=500, detail=str(e))
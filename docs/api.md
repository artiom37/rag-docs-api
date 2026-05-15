# API Documentation

Base URL:

```text
http://127.0.0.1:8000
```

---

## GET `/health`

Checks whether the backend is running.

### Request

```bash
curl http://127.0.0.1:8000/health
```

### Response

```json
{
  "status": "ok"
}
```

---

## POST `/ingest`

Ingests one or more documents into the vector index.

### Supported File Types

- `.txt`
- `.pdf`

### Request

```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"file_paths": ["data/raw/company_policy.txt", "data/raw/benefits.txt"]}'
```

### Request Body

```json
{
  "file_paths": ["data/raw/company_policy.txt", "data/raw/benefits.txt"]
}
```

### Response

```json
{
  "message": "Documents ingested successfully.",
  "docs": ["company_policy.txt", "benefits.txt"],
  "chunks_added": 2
}
```

---

## POST `/query`

Asks a question against ingested documents.

### Request

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "When are employees eligible for 401k matching?", "top_k": 4, "min_score": 0.4}'
```

### Request Body

```json
{
  "question": "When are employees eligible for 401k matching?",
  "top_k": 4,
  "min_score": 0.4
}
```

### Parameters

| Field       | Type    | Description                        |
| ----------- | ------- | ---------------------------------- |
| `question`  | string  | User question                      |
| `top_k`     | integer | Number of chunks to retrieve       |
| `min_score` | number  | Minimum similarity score threshold |

### Response

```json
{
  "answer": "Employees are eligible for 401(k) matching after 90 days of employment. (Source 1)",
  "sources": [
    {
      "doc_id": "benefits.txt",
      "chunk_id": "benefits.txt-chunk-0",
      "score": 0.438,
      "text": "The company offers medical, dental, and vision insurance..."
    }
  ]
}
```

---

## POST `/reset-index`

Clears the FAISS index and metadata.

This is useful during local development when documents have been ingested multiple times.

### Request

```bash
curl -X POST http://127.0.0.1:8000/reset-index
```

### Response

```json
{
  "message": "Vector index reset successfully."
}
```

---

## Error Handling

The API returns standard HTTP status codes.

| Status | Meaning                                 |
| ------ | --------------------------------------- |
| `200`  | Request succeeded                       |
| `400`  | Invalid request or unsupported document |
| `404`  | File not found                          |
| `500`  | Unexpected server error                 |

---

## Interactive API Docs

FastAPI automatically exposes OpenAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

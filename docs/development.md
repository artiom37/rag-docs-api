# Development Guide

## Local Backend Setup

Create virtual environment:

```bash
python -m venv .venv
```

Activate on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
python -m uvicorn app.main:app
```

---

## Docker Backend Setup

```bash
docker compose up --build
```

---

## Frontend Setup

```bash
cd ui
npm install
npm run dev
```

---

## Environment Variables

Create `.env` in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4.1-mini
```

---

## Common Commands

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Reset Index

```bash
curl -X POST http://127.0.0.1:8000/reset-index
```

### Ingest Documents

```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"file_paths": ["data/raw/company_policy.txt", "data/raw/benefits.txt"]}'
```

### Query

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "When are employees eligible for 401k matching?", "top_k": 4, "min_score": 0.4}'
```

---

## Git Hygiene

Do not commit:

- `.env`
- `.venv/`
- `data/index/`
- `ui/node_modules/`
- `ui/dist/`

Recommended `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc

data/index/

ui/node_modules/
ui/dist/

.DS_Store
```

---

## Troubleshooting

### Docker daemon is not running

Start Docker Desktop and verify:

```bash
docker version
```

### OpenAI quota error

Check OpenAI billing and usage limits.

### CORS error from React UI

Make sure FastAPI includes `CORSMiddleware` and allows:

```text
http://localhost:5173
http://127.0.0.1:5173
```

### Duplicate sources appear

Reset the vector index:

```bash
curl -X POST http://127.0.0.1:8000/reset-index
```

Then re-ingest documents.

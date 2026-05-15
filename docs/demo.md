# Demo Guide

This guide walks through a local demo of the RAG Docs API.

---

## 1. Start Backend

```bash
docker compose up --build
```

Verify:

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok"
}
```

---

## 2. Create Sample Documents

```bash
mkdir -p data/raw
```

```bash
cat > data/raw/company_policy.txt << 'EOF'
Employees may work remotely up to three days per week with manager approval.

Expense reports must be submitted within 30 days of the purchase date.

The company provides 15 days of paid vacation per calendar year.
EOF
```

```bash
cat > data/raw/benefits.txt << 'EOF'
The company offers medical, dental, and vision insurance.

Employees are eligible for 401(k) matching after 90 days of employment.

Parental leave is available for eligible full-time employees.
EOF
```

---

## 3. Reset Index

```bash
curl -X POST http://127.0.0.1:8000/reset-index
```

---

## 4. Ingest Documents

```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"file_paths": ["data/raw/company_policy.txt", "data/raw/benefits.txt"]}'
```

Expected:

```json
{
  "message": "Documents ingested successfully.",
  "docs": ["company_policy.txt", "benefits.txt"],
  "chunks_added": 2
}
```

---

## 5. Query Documents

### Ask About 401(k)

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "When are employees eligible for 401k matching?", "top_k": 4, "min_score": 0.4}'
```

Expected answer:

```text
Employees are eligible for 401(k) matching after 90 days of employment.
```

### Ask About Remote Work

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many remote work days are allowed?", "top_k": 4, "min_score": 0.4}'
```

Expected answer:

```text
Employees may work remotely up to three days per week with manager approval.
```

---

## 6. Start UI

```bash
cd ui
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Try asking:

```text
Tell me about 401k matching.
```

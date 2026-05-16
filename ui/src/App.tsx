import { useState } from "react";
import "./App.css";

type Source = {
  doc_id: string;
  chunk_id: string;
  score: number;
  text: string;
};

type QueryResponse = {
  answer: string;
  sources: Source[];
};

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [minScore, setMinScore] = useState(0.4);
  const [topK, setTopK] = useState(4);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion() {
    setLoading(true);
    setAnswer("");
    setSources([]);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          top_k: topK,
          min_score: minScore,
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data: QueryResponse = await response.json();

      setAnswer(data.answer);
      setSources(data.sources);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <section className="hero">
        <p className="eyebrow">RAG Docs API</p>
        <h1>Ask questions across your documents</h1>
        <p className="subtitle">
          FastAPI + OpenAI embeddings + FAISS vector search + grounded source
          citations.
        </p>
      </section>

      <section className="panel">
        <label htmlFor="question">Question</label>
        <textarea
          id="question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Example: When are employees eligible for 401k matching?"
        />

        <div className="controls">
          <label>
            Top K
            <input
              type="number"
              min={1}
              max={10}
              value={topK}
              onChange={(event) => setTopK(Number(event.target.value))}
            />
          </label>

          <label>
            Min Score
            <input
              type="number"
              min={0}
              max={1}
              step={0.05}
              value={minScore}
              onChange={(event) => setMinScore(Number(event.target.value))}
            />
          </label>
        </div>

        <button onClick={askQuestion} disabled={loading || !question.trim()}>
          {loading ? "Thinking..." : "Ask documents"}
        </button>

        {error && <p className="error">{error}</p>}
      </section>

      {answer && (
        <section className="card">
          <h2>Answer</h2>
          <p>{answer}</p>
        </section>
      )}

      {sources.length > 0 && (
        <section className="card">
          <h2>Sources</h2>
          <div className="sources">
            {sources.map((source) => (
              <article key={source.chunk_id} className="source">
                <div className="sourceHeader">
                  <strong>{source.doc_id}</strong>
                  <span>Score: {source.score.toFixed(3)}</span>
                </div>
                <p>{source.text}</p>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

export default App;

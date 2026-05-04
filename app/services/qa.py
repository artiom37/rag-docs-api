from typing import Any, Dict, List
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def build_context(search_results: List[tuple[float, Dict[str, Any]]]) -> str:
    blocks = []

    for i, (score, metadata) in enumerate(search_results, start=1):
        blocks.append(
            f"""
SOURCE {i}
doc_id: {metadata["doc_id"]}
chunk_id: {metadata["chunk_id"]}
score: {score}

{metadata["text"]}
""".strip()
        )

    return "\n\n---\n\n".join(blocks)


def answer_question(question: str, search_results: List[tuple[float, Dict[str, Any]]]) -> str:
    context = build_context(search_results)

    system_prompt = """
You are a careful RAG assistant.

Rules:
1. Answer only using the provided context.
2. If the answer is not in the context, say: "I don't know based on the provided documents."
3. Be concise.
4. Mention which source numbers support the answer.
""".strip()

    user_prompt = f"""
Question:
{question}

Context:
{context}
""".strip()

    response = client.responses.create(
        model=OPENAI_CHAT_MODEL,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.output_text
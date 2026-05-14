import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

import numpy as np
import faiss

from app.config import FAISS_INDEX_PATH, METADATA_PATH


class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if Path(FAISS_INDEX_PATH).exists():
            self.index = faiss.read_index(FAISS_INDEX_PATH)

        if Path(METADATA_PATH).exists():
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

    def _save(self):
        Path(FAISS_INDEX_PATH).parent.mkdir(parents=True, exist_ok=True)

        if self.index is not None:
            faiss.write_index(self.index, FAISS_INDEX_PATH)

        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

    def add(
        self,
        embeddings: List[List[float]],
        metadata: List[Dict[str, Any]],
    ):
        vectors = np.array(embeddings).astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(vectors)

        if self.index is None:
            dimension = vectors.shape[1]
            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)
        self.metadata.extend(metadata)

        self._save()

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 4,
    ) -> List[Tuple[float, Dict[str, Any]]]:
        if self.index is None or not self.metadata:
            return []

        query_vector = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            results.append((float(score), self.metadata[idx]))

        return results
    
    def reset(self) -> None:
        self.index = None
        self.metadata = []

        index_path = Path(FAISS_INDEX_PATH)
        metadata_path = Path(METADATA_PATH)

        if index_path.exists():
            index_path.unlink()

        if metadata_path.exists():
            metadata_path.unlink()


vector_store = VectorStore()
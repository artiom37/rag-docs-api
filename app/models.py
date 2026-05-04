from pydantic import BaseModel
from typing import List

class IngestRequest(BaseModel):
  file_path: str

class SourceChunk(BaseModel):
  doc_id: str
  chunk_id: str
  score: float
  text: str

class QueryRequest(BaseModel):
  question: str
  top_k: int = 4


class QueryResponse(BaseModel):
  answer: str
  sources: List[SourceChunk]
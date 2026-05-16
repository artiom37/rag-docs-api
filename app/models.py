from pydantic import BaseModel, Field
from typing import List

class IngestRequest(BaseModel):
  file_paths: List[str]

class SourceChunk(BaseModel):
  doc_id: str
  chunk_id: str
  score: float
  text: str

class QueryRequest(BaseModel):
  question: str
  top_k: int = Field(default=4, ge=1, le=10)
  min_score: float = Field(default=0.2, ge=0.0, le=1.0)


class QueryResponse(BaseModel):
  answer: str
  sources: List[SourceChunk]
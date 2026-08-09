from typing import List
from pydantic import BaseModel, Field

class RagQuestionRequest(BaseModel):
    query: str = Field(min_length=1)

class RagSource(BaseModel):
    document_name: str
    title: str
    section_title: str
    score: float
    source_urls: list[str] = []

class RagQuestionResponse(BaseModel):
    answer: str
    sources: List[RagSource]
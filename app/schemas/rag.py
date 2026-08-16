from typing import List
from pydantic import BaseModel, Field

class RagQuestionRequest(BaseModel):
    query: str = Field(min_length=1)
    session_id: str = Field(min_length=1)


class RagQuestionResponse(BaseModel):
    answer: str
    selected_program_id: str
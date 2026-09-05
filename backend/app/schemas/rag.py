from typing import List
from pydantic import BaseModel, Field

class RagQuestionRequest(BaseModel):
    query: str = Field(min_length=1)
    session_id: str = Field(min_length=1)


class ProgramDecisionRequest(BaseModel):
    session_id: str = Field(min_length=1)
    action:str

class RagQuestionResponse(BaseModel):
    answer: str
    selected_program_id: str | None = None

#đầu vào trả lời về thời gián muốn học (NN natural)cho LLM parser
class SchedulePreference(BaseModel):
    days_of_week: list[str]
    start_time: str | None = None
    end_time: str | None = None
    is_complete: bool
    clarification_question: str | None = None
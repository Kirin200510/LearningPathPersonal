from fastapi import APIRouter

from app.rag.rag_service import answer_question
from app.schemas.rag import (
    RagQuestionRequest,
    RagQuestionResponse,
)

router = APIRouter()

@router.post("/rag/ask")
def ask_question(request: RagQuestionRequest,)->RagQuestionResponse:
    answer = answer_question(question=request.query,session_id=request.session_id)
    return RagQuestionResponse(answer=answer)
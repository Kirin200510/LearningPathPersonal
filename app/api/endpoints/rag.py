from fastapi import APIRouter

from app.rag.rag_service import answer_question
from app.schemas.rag import (
    RagQuestionRequest,
    RagQuestionResponse,
)

router = APIRouter()

@router.post("/rag/ask")
def ask_question(request: RagQuestionRequest,)->RagQuestionResponse:
    result = answer_question(query=request.query,limit=3)
    return RagQuestionResponse(answer=result['answer'], sources=result['sources'])
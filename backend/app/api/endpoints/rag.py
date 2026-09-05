from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.rag.rag_service import answer_question,handle_program_decision
from app.schemas.rag import RagQuestionRequest,RagQuestionResponse,ProgramDecisionRequest
from app.api.deps import get_db,get_current_active_user
from app.model.user import User


router = APIRouter()

@router.post("/rag/ask/")
def ask_question(request: RagQuestionRequest,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_db))->RagQuestionResponse:
    answer = answer_question(question=request.query,session_id=request.session_id,user_id=current_user.id,db=db)
    return RagQuestionResponse(**answer)

@router.post("/rag/program-decision/")
def program_decision(request: ProgramDecisionRequest,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    return handle_program_decision(session_id=request.session_id,action=request.action,user_id=current_user.id,db=db)
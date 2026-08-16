from dataclasses import dataclass

from app.schemas.rag import RagQuestionRequest


@dataclass
class ConversationState:
    selected_program_id:str
    stage:str = "Chat"

stage_store:dict[str,ConversationState]={}

def get_conversation_state(session_id:str)->ConversationState:
    if session_id not in stage_store:
        stage_store[session_id] = ConversationState()
    return stage_store[session_id]
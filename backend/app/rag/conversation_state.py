from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class ConversationState():
    selected_program_id: str | None = None
    learning_path_id: int | None = None

    stage: str = "CHAT"

    days_of_week: list[str] | None = None
    start_time: str | None = None
    end_time: str | None = None

stage_store:dict[str,ConversationState]={}

def get_conversation_state(session_id:str)->ConversationState:
    if session_id not in stage_store:
        stage_store[session_id] = ConversationState()
    return stage_store[session_id]
from langchain_core.chat_history import  BaseChatMessageHistory,InMemoryChatMessageHistory


history_store:dict[str,InMemoryChatMessageHistory]={}

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in history_store:
        history_store[session_id]=InMemoryChatMessageHistory()
    return history_store[session_id]

def clear_session_history(session_id:str)->None:
    history=history_store.get(session_id)
    if history:
        history.clear()

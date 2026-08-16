from app.rag.chain import get_rag_chain

def answer_question(question: str,session_id: str) -> str:

    question = question.strip()
    session_id = session_id.strip()

    if not question or not session_id:
        raise ValueError(
            "Question, Session ID cannot be empty."
        )


    rag_chain = get_rag_chain()
    answer = rag_chain.invoke(
        {
        "question":question
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )
    return answer
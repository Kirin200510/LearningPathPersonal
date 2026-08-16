from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory

from app.rag.chat_history import get_session_history
from app.rag.conversation_state import get_conversation_state
from app.rag.intent_router import classify_intent
from app.rag.llm import get_llm
from app.rag.prompt import get_rag_prompt
from app.rag.retriever import get_retriever, retrieve_catalog_programs


def format_docs(docs) -> str:
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def format_program(programs: list[dict]) -> str:
    program_blocks = []
    for program in programs:
        learning_items = program.get("learning_items")
        item_lines = []

        for item in learning_items:
            item_lines.append(f'{item.get("order")}. 'f'{item.get("title")}')

        curriculum = "\n".join(item_lines)
        block = f"""
        Program ID:
        {program.get("source_id")}
        
        Program:
        {program.get("title")}

        Description:
        {program.get("description")}

        URL:
        {program.get("url")}

        Learning items:
        {curriculum}
        """.strip()

        program_blocks.append(block)
    return "\n\n".join(program_blocks)


def retrieve_context(inputs:dict) -> str:
    question = inputs["question"]
    history = inputs.get("history")
    #total  1 question including history
    retrieval_query=build_retrieval_query(question,history)
    intent=classify_intent(retrieval_query)
    if intent=="CAREER":
        retriever = get_retriever(intent="CAREER",k=3)
        documents=retriever.invoke(retrieval_query)
        return format_docs(documents)

    elif intent=="LEARNING":
        programs=retrieve_catalog_programs(query=retrieval_query,k=5)
        return format_program(programs)
    else:
        raise ValueError("Intent không hợp lệ")




def get_rag_chain():

    llm = get_llm()
    prompt = get_rag_prompt()
    rag_chain = (
            {
                "context": RunnableLambda(
                    retrieve_context
                ),
                # all history
                "history": RunnableLambda(
                    lambda x: x.get("history")
                ),
                "question": RunnableLambda(
                    lambda x: x["question"]
                )
            }
            | prompt
            | llm
            | StrOutputParser()
    )
    chain_with_history = (
        RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )
    )
    return chain_with_history

#Xử lý trường hợp hỏi chưa rõ ràng
def build_retrieval_query(question: str,history: list[BaseMessage]) -> str:
    # top 4 near message in session
    recent_history=history[-4:]
    parts = []

    for message in recent_history:
        if message.content:
            parts.append(str(message.content))
    parts.append(question)
    return "\n".join(parts)


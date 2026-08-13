from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Bạn là trợ lý tư vấn lộ trình học Công nghệ thông tin. "
            "Chỉ trả lời dựa trên CONTEXT được cung cấp. "
            "Nếu CONTEXT không đủ thông tin, hãy nói rõ rằng chưa có đủ thông tin.",
        ),
        (
            "human",
            "CONTEXT:\n{context}\n\nQUESTION:\n{question}",
        ),
    ]
)


def get_rag_prompt() -> ChatPromptTemplate:
    return RAG_PROMPT

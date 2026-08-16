from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from openai import RateLimitError
from app.rag.llm import get_llm

VALID_INTENTS = {
    "CAREER",
    "LEARNING"
}

def get_intent_prompt() -> ChatPromptTemplate:
    system_prompt = """
Bạn có nhiệm vụ phân loại câu hỏi của người dùng
trong hệ thống tư vấn học tập và nghề nghiệp ngành CNTT.

Phân loại dựa trên THÔNG TIN MÀ NGƯỜI DÙNG MUỐN NHẬN,
không chỉ dựa trên các từ xuất hiện trong câu hỏi.

Có 2 loại:

CAREER:
Người dùng muốn biết thông tin về nghề nghiệp,
ví dụ:
- nghề đó làm gì
- công việc thường gặp
- kỹ năng nghề yêu cầu
- nền tảng cần có
- nghề phù hợp với ai
- các nghề liên quan
- định hướng nghề nghiệp

LEARNING:
Người dùng muốn biết cách học hoặc tài nguyên học,
ví dụ:
- nên học gì
- nên học lộ trình nào
- có khóa học nào phù hợp
- học công nghệ nào
- chương trình học nào
- tài liệu hoặc nơi học

Ví dụ:

"Backend Developer làm gì?"
→ CAREER

"Backend Developer cần kỹ năng gì?"
→ CAREER

"Tôi muốn trở thành Backend Developer thì nên học lộ trình nào?"
→ LEARNING

"Có khóa học React nào không?"
→ LEARNING

Chỉ trả về đúng một trong hai giá trị:

CAREER
LEARNING

Không giải thích thêm.
""".strip()
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )

def fallback_classify_intent(
    question: str,
) -> str:
    question = question.lower()

    learning_keywords = [
        "học",
        "khóa học",
        "khoá học",
        "lộ trình",
        "tài liệu",
        "chương trình học",
        "học ở đâu",
    ]

    for keyword in learning_keywords:
        if keyword in question:
            return "LEARNING"

    return "CAREER"

def classify_intent(question: str) -> str:
    question = question.strip()
    chain=get_intent_prompt()| get_llm()|StrOutputParser()
    try:
        intent = chain.invoke(
            {
                "question": question,
            })
    except RateLimitError:
        print(
            "LLM bị rate limit, dùng fallback."
        )
        return fallback_classify_intent(question)

    intent = intent.strip().upper()

    if intent not in VALID_INTENTS:
        raise ValueError("Câu hỏi không liên quan")

    return intent



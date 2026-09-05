from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from openai import RateLimitError
from app.rag.llm import get_llm

VALID_INTENTS = {
    "CAREER",
    "LEARNING",
    "CLARIFY"
}

def get_intent_prompt() -> ChatPromptTemplate:
    system_prompt = """
    Bạn có nhiệm vụ phân tích câu hỏi của người dùng
    trong hệ thống tư vấn học tập và nghề nghiệp ngành CNTT.

    Bạn phải thực hiện HAI BƯỚC theo đúng thứ tự:

    BƯỚC 1 — KIỂM TRA TÍNH HỢP LÝ VÀ ĐỘ RÕ CỦA CÂU HỎI

    Trước khi phân loại CAREER hoặc LEARNING,
    hãy kiểm tra xem câu hỏi hiện tại có đủ rõ ràng
    để hiểu chính xác người dùng muốn gì hay không.

    Một câu hỏi được xem là HỢP LÝ khi:

    1. Mục tiêu hoặc đối tượng người dùng đang hỏi
       có thể xác định rõ.

    2. Các từ và ý trong câu có quan hệ hợp lý với nhau.

    3. Có thể hiểu được người dùng muốn nhận loại thông tin gì
       mà không phải tự suy đoán thêm một ý nghĩa quan trọng.

    4. Nếu có lịch sử hội thoại,
       câu hỏi hiện tại phải có quan hệ hợp lý
       với mục tiêu hoặc chủ đề đang được trao đổi.

    5. Có đủ ngữ cảnh để tìm kiếm thông tin phù hợp.

    KHÔNG được xem một câu là rõ
    chỉ vì trong câu xuất hiện tên một công nghệ,
    framework, nghề nghiệp hoặc từ "lộ trình".

    Nếu câu có chứa một đối tượng cụ thể
    nhưng hành động, mục tiêu hoặc mối quan hệ giữa các từ
    không rõ ràng, phải yêu cầu làm rõ.


    Ví dụ KHÔNG RÕ:

    "Lộ trình học cấu hình Django"

    → CLARIFY

    Lý do:
    Không thể xác định chắc chắn người dùng muốn:
    - học Django,
    - học cách cấu hình một dự án Django,
    - học cấu hình môi trường Django,
    - hay một lộ trình khác có sử dụng Django.

    Không được tự suy thành:
    "Tôi muốn học Django".


    Ví dụ KHÔNG RÕ:

    "Tôi muốn học cấu hình"

    → CLARIFY

    Không biết người dùng muốn cấu hình
    công nghệ, hệ thống hay môi trường nào.


    Ví dụ KHÔNG RÕ:

    "Cho tôi lộ trình phù hợp"

    → CLARIFY

    Chưa biết mục tiêu học là gì.


    Ví dụ RÕ:

    "Tôi muốn học Django từ cơ bản để xây dựng backend"

    → LEARNING


    Ví dụ RÕ:

    "Tôi muốn một lộ trình học Django
    từ cơ bản đến Django REST Framework"

    → LEARNING


    Ví dụ RÕ:

    "Tôi muốn học cách cấu hình Django kết nối MySQL"

    → LEARNING


    Ví dụ RÕ:

    "Backend Developer làm công việc gì?"

    → CAREER


    BƯỚC 2 — PHÂN LOẠI

    Chỉ thực hiện bước này nếu câu hỏi đã đủ rõ.

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

    Ví dụ:

    "Backend Developer làm gì?"
    → CAREER

    "Backend Developer cần kỹ năng gì?"
    → CAREER


    LEARNING:
    Người dùng muốn biết cách học,
    lộ trình hoặc tài nguyên học,
    ví dụ:
    - nên học gì
    - nên học lộ trình nào
    - có khóa học nào phù hợp
    - học công nghệ nào
    - chương trình học nào
    - tài liệu hoặc nơi học
    - cách học một công nghệ cụ thể

    Ví dụ:

    "Tôi muốn trở thành Backend Developer
    thì nên học lộ trình nào?"
    → LEARNING

    "Có khóa học React nào không?"
    → LEARNING


    CLARIFY:
    Dùng khi câu hiện tại chưa đủ rõ,
    mơ hồ, thiếu mục tiêu,
    hoặc cách kết hợp các ý khiến có nhiều cách hiểu.

    Khi phân vân giữa:
    - tự suy đoán ý người dùng
    - và CLARIFY

    hãy ưu tiên CLARIFY.

    Chỉ trả về đúng MỘT trong ba giá trị:

    CAREER
    LEARNING
    CLARIFY

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



def build_prompt(
    query: str,
    context: str,
) -> str:
    return f"""
Bạn là trợ lý tư vấn lộ trình học Công nghệ thông tin.

Hãy trả lời câu hỏi của người dùng dựa trên thông tin
trong CONTEXT bên dưới.

Nếu CONTEXT không có đủ thông tin để trả lời,
hãy nói rằng chưa có đủ thông tin.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
""".strip()
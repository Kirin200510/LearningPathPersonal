from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.rag.llm import get_llm
from app.schemas.rag import SchedulePreference


def parse_schedule_preference(text: str) -> SchedulePreference:
    parser = PydanticOutputParser(pydantic_object=SchedulePreference)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Bạn có nhiệm vụ trích xuất thời gian học
từ câu nói tự nhiên của người dùng.

Quy tắc:

- Chuẩn hóa ngày trong tuần thành:
  monday
  tuesday
  wednesday
  thursday
  friday
  saturday
  sunday

- Chuẩn hóa giờ thành định dạng HH:MM 24 giờ.

Ví dụ:
"5 giờ chiều" -> "17:00"
"9 giờ tối" -> "21:00"
"7h sáng" -> "07:00"

- Không tự suy đoán thông tin người dùng chưa nói.

- is_complete = true chỉ khi đã có:
  + ít nhất một ngày học
  + start_time
  + end_time

- Nếu thiếu thông tin:
  is_complete = false
  và clarification_question phải là
  một câu hỏi ngắn để hỏi đúng thông tin còn thiếu.

{format_instructions}
""",
            ),
            (
                "human",
                "{text}",
            ),
        ]
    )
    chain = (
            prompt
            | get_llm()
            | parser
    )
    return chain.invoke(
        {
            "text": text,
            "format_instructions": (
                parser.get_format_instructions()
            ),
        }
    )


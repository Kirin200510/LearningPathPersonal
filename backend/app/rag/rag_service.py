from app.rag.chain import get_rag_chain
from app.rag.conversation_state import get_conversation_state
from app.rag.schedule_parser import parse_schedule_preference
from sqlalchemy.orm import Session
from app.rag.learning_path_builder import create_learning_path_from_program
from app.rag.scheduler import create_personal_schedule,generate_schedule,check_schedule_conflict

from app.model.learning_path import LearningPath


def answer_question(question: str,session_id: str,user_id:int,db:Session) -> dict:

    question = question.strip()
    session_id = session_id.strip()

    if not question or not session_id:
        raise ValueError(
            "Question, Session ID cannot be empty."
        )
    #LLM phân tích schedule
    state = get_conversation_state(session_id)
    if state.stage=="WAITING_FOR_SCHEDULE":
        schedule=parse_schedule_preference(question)
        if schedule.days_of_week:
            state.days_of_week=schedule.days_of_week
        if schedule.start_time:
            state.start_time=schedule.start_time
        if schedule.end_time:
            state.end_time=schedule.end_time

        #Kiểm tra input
        schedule_complete=(state.days_of_week and state.start_time and state.end_time)
        if not schedule_complete:
            return {
                "answer":schedule.clarification_question,
                "selected_program_id": state.selected_program_id
            }
        existing_path = (db.query(LearningPath).filter(
            LearningPath.user_id == user_id,
            LearningPath.program_source_id == state.selected_program_id)
            .first()
        )

        if existing_path:
            state.stage = "CHAT"
            state.selected_program_id = None
            state.days_of_week = None
            state.start_time = None
            state.end_time = None

            return {
                "answer": "Bạn đã tạo lộ trình này trước đây.",
                "selected_program_id": None
            }

        try:
            learning_path=create_learning_path_from_program(db=db,user_id=user_id,program_source_id=state.selected_program_id)
            planned_schedules=generate_schedule(db=db,learning_path_id=learning_path.id,days_of_week=state.days_of_week,start_time=state.start_time,end_time=state.end_time)
            conflicts=check_schedule_conflict(db=db,user_id=user_id,planned_schedules=planned_schedules)
            if conflicts:
                db.rollback()
                conflict=conflicts[0]
                return {
                    "answer": (
                        "Lịch học bạn chọn bị trùng với lịch đã có vào ngày "
                        f"{conflict['scheduled_date'].strftime('%d/%m/%Y')} "
                        "từ "
                        f"{conflict['start_time'].strftime('%H:%M')} "
                        "đến "
                        f"{conflict['end_time'].strftime('%H:%M')}. "
                        "Bạn hãy chọn ngày hoặc khung giờ khác."
                    ),
                    "selected_program_id":None
                }

            #Khong trung
            create_personal_schedule(db=db,user_id=user_id, planned_schedules=planned_schedules)
            db.commit()
            state.learning_path_id=learning_path.id
            state.stage="SCHEDULED"
            return {
                "answer": "Đã tạo lộ trình học và lịch học cho bạn",
                "selected_program_id":None
            }
        except:
            db.rollback()
            raise

    #normal rag
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
    #lấy đoạn hội thoại từ chat session
    selected_program_id=answer.get("selected_program_id")
    if selected_program_id:
        state.selected_program_id=selected_program_id
        state.stage=" WAITING_CONFIRMATION"


    return answer

#confirm/reject learning path(advise)
def handle_program_decision(session_id: str,action:str,user_id:int,db:Session) -> dict:
    state=get_conversation_state(session_id)
    if state.stage!=" WAITING_CONFIRMATION":
        raise ValueError("Không có lộ trình nào cần confirm")
    if not state.selected_program_id:
        raise ValueError("Không có lộ trình")

    action=action.strip().lower()
    if action=="confirm":
        existing_path = (db.query(LearningPath)
                         .filter(LearningPath.user_id == user_id,
                                LearningPath.program_source_id == state.selected_program_id)
                         .first()
        )

        if existing_path:
            state.stage = "CHAT"
            state.selected_program_id = None
            state.days_of_week = None
            state.start_time = None
            state.end_time = None

            return {
                "answer": "Bạn đã tạo lộ trình này trước đây.",
                "selected_program_id": None
            }


        state.stage="WAITING_FOR_SCHEDULE"
        state.days_of_week = None
        state.start_time = None
        state.end_time = None
        return {
            "answer": "Lộ trình đã được xác nhận. Bạn muốn học vào những ngày nào và khung giờ nào trong tuần?",
            "selected_program_id": state.selected_program_id
        }
    elif action=="reject":
        state.selected_program_id = None
        state.days_of_week = None
        state.start_time = None
        state.end_time = None
        state.stage = "CHAT"
        return {
            "answer": "Đã từ chối lộ trình",
            "selected_program_id": None
        }
    else:
        raise ValueError("Error")

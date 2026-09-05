from datetime import date, datetime, time, timedelta

from sqlalchemy.orm import Session
from app.model.course import Course
from app.model.learning_path import PathNode
from app.model.personal_schedule import PersonalSchedule

DAY_TO_INDEX = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}
#kiểm tra trùng lịch
def check_schedule_conflict(db: Session, user_id: int,planned_schedules: list[dict]) -> list[dict]:
    conflicts = []
    for item in planned_schedules:
        overlapping = (
            db.query(PersonalSchedule)
            .filter(
                PersonalSchedule.user_id == user_id,
                PersonalSchedule.scheduled_date== item["scheduled_date"],
                PersonalSchedule.start_time< item["end_time"],
                PersonalSchedule.end_time> item["start_time"]
            )
            .first()
        )
        if overlapping:
            conflicts.append(
                {
                    "course_id": item["course_id"],
                    "scheduled_date":item["scheduled_date"],
                    "start_time": item["start_time"],
                    "end_time":item["end_time"],
                    "conflict_schedule_id":overlapping.id
                }
            )
    return conflicts

def generate_schedule(db:Session,learning_path_id:int,days_of_week:list[str],start_time:str,end_time:str,start_date: date | None = None) -> list[dict]:
    if not days_of_week:
        raise ValueError("days_of_week must not be empty")

    start_clock=time.fromisoformat(start_time)
    end_clock=time.fromisoformat(end_time)
    if start_clock >= end_clock:
        raise ValueError("start_clock must be less than end_clock")

    session_hours = (datetime.combine(date.today(),end_clock)-datetime.combine(date.today(),start_clock)).total_seconds() / 3600

    day_indexes=[]
    for day in days_of_week:
        day=day.lower()
        if day not in DAY_TO_INDEX:
            raise ValueError("Lỗi date")

        day_indexes.append(DAY_TO_INDEX[day])

    #Lấy course theo thứ tự in learning path
    course_orders=(db.query(PathNode,Course)
                   .join(Course,Course.id==PathNode.course_id)
                   .filter(PathNode.learning_path_id==learning_path_id)
                   .order_by(PathNode.sequence_order)
                   .all()
                   )
    if not course_orders:
        raise ValueError("Learning path không có Course")

    schedules=[]
    current_date=start_date or date.today()
    for node, course in course_orders:
        if (course.estimated_hours is None or course.estimated_hours <= 0):
           remaining_hours=session_hours
        #total hours to learn 1 course
        else:
            remaining_hours = float(course.estimated_hours)
        while remaining_hours > 0:
            while (current_date.weekday()not in day_indexes):
                current_date += timedelta(days=1)

            current_session_hours = min(session_hours,remaining_hours)
            # buoi cuoi co the ngan hon
            actual_end_datetime = (datetime.combine(current_date,start_clock) +timedelta(hours=current_session_hours))
            actual_end_time = (actual_end_datetime.time())

            schedules.append(
                {
                    "course_id": course.id,
                    "title": course.title,
                    "url": course.url,
                    "sequence_order": node.sequence_order,
                    "scheduled_date":current_date,
                    "start_time":start_clock,
                    "end_time": actual_end_time,
                    "learning_path_id": node.learning_path_id,
                }
            )
            # Trừ số giờ vừa học
            remaining_hours -= (current_session_hours)
            # Course/buổi tiếp theo tìm ngay tiep theo
            current_date += timedelta(days=1)
    return schedules

def create_personal_schedule(db: Session,user_id: int,planned_schedules: list[dict]) -> list[PersonalSchedule]:
    personal_schedules = []
    for item in planned_schedules:
        schedule = PersonalSchedule(
            user_id=user_id,
            course_id=item["course_id"],
            scheduled_date=item["scheduled_date"],
            start_time=item["start_time"],
            end_time=item["end_time"],
            is_reminder_enabled=True,
            learning_path_id=item["learning_path_id"],
        )
        personal_schedules.append(schedule)

    db.add_all(personal_schedules)
    db.flush()
    return personal_schedules
from sqlalchemy.orm import Session
from sympy import sequence

from app.model.course import Course
from app.model.learning_path import LearningPath,PathNode
from app.rag.catalog_parent import get_program_by_source_id

def get_item_estimated_hours(item: dict) -> float | None:
    estimated_hours = item.get("estimated_hours")
    if estimated_hours:
        return float(estimated_hours)

    duration_minutes=item.get("duration_minutes")
    if duration_minutes:
        return float(duration_minutes)/60

    duration_weeks=item.get("duration_weeks")
    effort_hours=item.get("effort_hours_per_week")
    if effort_hours and duration_weeks:
        return float(duration_weeks*effort_hours)
    return None
#order course
def get_order(item):
    return item.get("order")

def create_learning_path_from_program(db: Session,user_id: int,program_source_id: str)->LearningPath:
    program=get_program_by_source_id(program_source_id)
    if not program:
        raise ValueError("No program")

    #Get learning item in program
    learning_items=program.get("learning_items")
    if not learning_items:
        raise ValueError("No learning items")
    learning_items=sorted(learning_items,key=get_order)

    learning_path=LearningPath(user_id=user_id,url=program.get("url"),program_source_id=program_source_id)
    db.add(learning_path)
    db.flush()

    #create course,pathnode
    for index,item in enumerate(learning_items):
        item_source_id=item.get("source_id")
        if not item_source_id:
            item_source_id = f"{program_source_id}:"f"{item.get('order', index + 1)}"

        course=db.query(Course).filter(Course.source_id==item_source_id).first()
        if not course:
            course=Course(source_id=item_source_id,
                          title=item.get("title"),
                          description=item.get("description"),
                          url=item.get("url"),
                          estimated_hours=get_item_estimated_hours(item)
                          )
            db.add(course)
            db.flush()

        node=PathNode(
            learning_path_id=learning_path.id,
            course_id=course.id,
            sequence_order=item.get('order')
        )
        db.add(node)

    db.flush()
    return learning_path









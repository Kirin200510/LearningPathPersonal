from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_valid_lesson_for_user, check_and_unlock_next_course
from app.db.base import ProgressStatus
from app.model.lesson import Lesson, LessonProgress
from app.schemas.lesson import LessonResponse,LessonProgressResponse,LessonProgressUpdate
from app.api.deps import get_db, get_current_user
from app.model.user import User

router = APIRouter()

@router.get("/lessons/{id}/")
def get_lesson_content(
    lesson: Lesson = Depends(get_valid_lesson_for_user))->LessonResponse:
    return lesson

@router.post("/lessons/{id}/progress/")
def update_lesson_progress(id: int,data: LessonProgressUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user))->LessonProgressResponse:
    lesson=db.query(Lesson).filter(Lesson.id == id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = db.query(LessonProgress).filter(LessonProgress.user_id == current_user.id,LessonProgress.lesson_id == id).first()
    if not progress:
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=id,
            watched_seconds=0,
            status=ProgressStatus.IN_PROGRESS
        )
        db.add(progress)

    if data.watched_seconds > progress.watched_seconds:
        progress.watched_seconds = data.watched_seconds

    is_next_course_unlocked = False

    if lesson.duration_seconds > 0 and progress.status != ProgressStatus.COMPLETED :
        percent = (progress.watched_seconds / lesson.duration_seconds) * 100

        if percent>=80:
            progress.status = ProgressStatus.COMPLETED
            is_next_course_unlocked = check_and_unlock_next_course(db, current_user.id, lesson.course_id)

    db.commit()

    return LessonProgressResponse(
        lesson_id=progress.lesson_id,
        watched_seconds=progress.watched_seconds,
        status=progress.status,
        is_next_course_unlocked=is_next_course_unlocked
    )


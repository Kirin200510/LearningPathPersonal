from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi_pagination.ext.sqlalchemy import paginate

from app.api.deps import get_db,get_current_active_user
from app.db.base import PathStatus, ProgressStatus
from app.model.course import Course, CoursePrerequisite
from app.model.learning_path import PathNode, LearningPath
from app.model.lesson import Lesson, LessonProgress
from app.model.user import User
from app.schemas.course import CourseResponse, CourseProgressResponse
from app.schemas.lesson import LessonBase

router = APIRouter()
CoursePage = CustomizedPage[
    Page[CourseResponse],
    UseParamsFields(size=Query(10, ge=1, le=100))
]

@router.get("/courses/")
def get_courses(search: Optional[str]=None, skill_id: Optional[str]=None,db: Session = Depends(get_db)) -> CoursePage:
    query = db.query(Course)
    if search:
        query = query.filter(Course.title.ilike(f"%{search}%"))
    return paginate(db,query)

@router.get("/courses/{id}/")
def get_course_detail(id: int, db: Session = Depends(get_db)) -> CourseResponse:
    course = db.query(Course).options(joinedload(Course.skills)).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/{id}/lessons/")
def get_course_lessons(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_active_user))->List[LessonBase]:
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.lessons

@router.get("/courses/{id}/prerequisites/")
def get_course_prerequisites(id: int, db: Session = Depends(get_db))->List[CourseResponse]:
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    prerequisites = (db.query(Course).join(CoursePrerequisite,Course.id == CoursePrerequisite.prerequisite_course_id)
                     .filter(CoursePrerequisite.course_id == id).all())
    return prerequisites

@router.get("/courses/{id}/progress/")
def get_course_progress(id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_active_user)) -> CourseProgressResponse:
    node=(db.query(PathNode).join(LearningPath)
          .filter(LearningPath.user_id == current_user.id,LearningPath.status == PathStatus.ACTIVE,PathNode.course_id == id)
          .first())

    if not node:
        raise HTTPException(status_code=404, detail="Course not found in path")

    total_lessons = db.query(Lesson).filter(Lesson.course_id == id).count()
    completed_lessons = (db.query(LessonProgress).join(Lesson)
                         .filter(LessonProgress.user_id == current_user.id,Lesson.course_id == id,LessonProgress.status == ProgressStatus.COMPLETED)
                         .count())
    progress_percentage = 0.0
    if total_lessons > 0:
        progress_percentage = round((completed_lessons / total_lessons) * 100, 2)

    return CourseProgressResponse(
        course_id=id,
        status=node.status,
        is_unlocked=node.is_unlocked,
        total_lessons=total_lessons,
        completed_lessons=completed_lessons,
        progress_percentage=progress_percentage
    )

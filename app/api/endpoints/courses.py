from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi_pagination.ext.sqlalchemy import paginate

from app.api.deps import get_db
from app.model.course import Course, CoursePrerequisite
from app.schemas.course import CourseResponse

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

@router.get("/courses/{id}/prerequisites/")
def get_course_prerequisites(id: int, db: Session = Depends(get_db))->List[CourseResponse]:
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    prerequisites = (db.query(Course).join(CoursePrerequisite,Course.id == CoursePrerequisite.prerequisite_course_id)
                     .filter(CoursePrerequisite.course_id == id).all())
    return prerequisites



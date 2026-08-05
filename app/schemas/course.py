from pydantic import BaseModel
from typing import Optional,List
from app.db.base import ProgressStatus

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_hours: Optional[int] = None

class CourseSkillDetail(BaseModel):
    skill_id: int

    class Config:
        from_attributes = True

class CourseResponse(CourseBase):
    id: int
    skills: List[CourseSkillDetail]

    class Config:
        from_attributes= True

class CourseProgressResponse(BaseModel):
    course_id: int
    status: ProgressStatus
    is_unlocked: bool
    total_lessons: int
    completed_lessons: int
    progress_percentage: float

from pydantic import BaseModel
from typing import Optional,List

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


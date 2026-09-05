from pydantic import BaseModel
from typing import Optional,List

class CourseBase(BaseModel):
    source_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    estimated_hours: Optional[int] = None
    url: Optional[str] = None


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes= True


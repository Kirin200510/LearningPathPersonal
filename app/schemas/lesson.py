from pydantic import BaseModel
from typing import Optional
from app.db.base import ProgressStatus

class LessonBase(BaseModel):
    id: int
    title: str
    duration_seconds: int = 0
    sequence_order: int

    class Config:
        from_attributes = True


class LessonDetail(LessonBase):
    content_type: Optional[str] = None
    content_url: Optional[str] = None

    class Config:
        from_attributes = True

class LessonResponse(LessonBase):
    course_id: int
    content: Optional[str] = None
    video_url: Optional[str] = None

    class Config:
        from_attributes = True

#Update progress lesson
class LessonProgressUpdate(BaseModel):
    watched_seconds: int

class LessonProgressResponse(BaseModel):
    lesson_id: int
    watched_seconds: int
    status: ProgressStatus
    is_next_course_unlocked: bool = False



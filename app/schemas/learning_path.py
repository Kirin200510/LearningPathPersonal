from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from app.db.base import PathStatus,ProgressStatus

class LearningPathCreate(BaseModel):
    career_goal_id: Optional[int]=None
    course_ids: List[int]

class LearningPathResponse(BaseModel):
    id:int
    user_id:int
    career_goal_id:Optional[int]
    status: PathStatus
    created_at: datetime

    class Config:
        from_attributes = True

class LearningPathProgressResponse(BaseModel):
    learning_path_id: int
    total_courses: int
    completed_courses: int
    progress_percentage: float

class PathNodeResponse(BaseModel):
    id: int
    learning_path_id: int
    course_id: int
    sequence_order: int
    is_unlocked: bool
    status: ProgressStatus

    class Config:
        from_attributes = True


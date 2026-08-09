from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime


class LearningPathCreate(BaseModel):
    career_goal_id: Optional[int]=None
    course_ids: List[int]

class LearningPathResponse(BaseModel):
    id:int
    user_id:int
    career_goal_id:Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class PathNodeResponse(BaseModel):
    id: int
    learning_path_id: int
    course_id: int
    sequence_order: int

    class Config:
        from_attributes = True


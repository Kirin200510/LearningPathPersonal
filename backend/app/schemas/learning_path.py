from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LearningPathResponse(BaseModel):
    id:int
    user_id:int
    created_at: datetime
    url: Optional[str] = None

    class Config:
        from_attributes = True


class PathNodeResponse(BaseModel):
    id: int
    learning_path_id: int
    course_id: int
    sequence_order: int

    class Config:
        from_attributes = True


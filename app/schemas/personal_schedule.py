from pydantic import BaseModel
from datetime import time
from typing import Optional,List

class ScheduleBase(BaseModel):
    course_id: int
    start_time: time
    end_time: time
    is_reminder_enabled: Optional[bool] = True


class ScheduleCreate(ScheduleBase):
    days_of_week: List[int]

class ScheduleResponse(ScheduleBase):
    id: int
    user_id: int
    day_of_week: int

    class Config:
        from_attributes = True

class ScheduleUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_reminder_enabled: Optional[bool] = None
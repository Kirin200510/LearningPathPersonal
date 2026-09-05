from pydantic import BaseModel
from datetime import time,date
from typing import Optional,List

class ScheduleBase(BaseModel):
    course_id: int
    start_time: time
    end_time: time
    scheduled_date: date
    is_reminder_enabled: Optional[bool] = True

class ScheduleResponse(ScheduleBase):
    id: int
    user_id: int
    learning_path_id: int


    class Config:
        from_attributes = True

class ScheduleUpdate(BaseModel):
    scheduled_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_reminder_enabled: Optional[bool] = None
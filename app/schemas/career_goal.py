from pydantic import BaseModel
from typing import Optional, List
from app.schemas.skill import SkillResponse

class CareerGoalBase(BaseModel):
    title: str
    description: Optional[str] = None

class CareerGoalResponse(CareerGoalBase):
    id: int

    class Config:
        from_attributes= True

class GoalSkillDetail(BaseModel):
    weight: int
    skills: SkillResponse

    class Config:
        from_attributes = True


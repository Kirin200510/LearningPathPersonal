from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session,joinedload
from typing import List

from app.api.deps import get_db
from app.model.career_goal import CareerGoal
from app.model.skill import Skill, GoalSkill
from app.schemas.career_goal import CareerGoalResponse, GoalSkillDetail
from app.schemas.skill import SkillResponse

from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter()

# customize page
CareerGoalPage = CustomizedPage[
    Page[CareerGoalResponse],
    UseParamsFields(size=Query(10, ge=1, le=100))]

SkillPage = CustomizedPage[
    Page[SkillResponse],
    UseParamsFields(size=Query(10, ge=1, le=100))
]

@router.get("/career-goals/")
def get_career_goals(db: Session = Depends(get_db)) -> CareerGoalPage:
    query = db.query(CareerGoal)
    return paginate(db, query)

@router.get("/career-goals/{id}/skills/")
def get_career_goal_skills(id: int, db: Session = Depends(get_db)) -> List[GoalSkillDetail]:
    # Tránh lazy load
    goal = db.query(CareerGoal).options(joinedload(CareerGoal.skills).joinedload(GoalSkill.skills)).filter(CareerGoal.id == id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Career goal not found")
    return goal.skills

@router.get("/skills/")
def get_skills(db: Session = Depends(get_db)) -> SkillPage:
    query = db.query(Skill)
    return paginate(db, query)




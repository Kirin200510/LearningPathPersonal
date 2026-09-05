from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_active_user
from app.model.learning_path import PathNode,LearningPath
from app.model.personal_schedule import PersonalSchedule
from app.model.course import Course
from app.schemas.personal_schedule import ScheduleResponse,ScheduleUpdate
from app.model.user import User

router = APIRouter()

@router.get("/schedules/me")
def get_schedules(db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user))->List[ScheduleResponse]:
    schedules=db.query(PersonalSchedule).filter(PersonalSchedule.user_id == current_user.id).all()
    return schedules

@router.patch("/schedules/me/{id}/")
def update_user_schedule(id:int,data:ScheduleUpdate,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_db))->ScheduleResponse:
    schedule = db.query(PersonalSchedule).filter(
        PersonalSchedule.id == id,
        PersonalSchedule.user_id == current_user.id
    ).first()

    if not schedule:
        raise HTTPException(status_code=404)

    # chỉ update những thuộc tính cần update
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return schedule

    new_day = update_data.get("scheduled_date", schedule.scheduled_date)
    new_start = update_data.get("start_time", schedule.start_time)
    new_end = update_data.get("end_time", schedule.end_time)

    if new_start >= new_end:
        raise HTTPException(status_code=400)

    if "scheduled_date" in update_data or "start_time" in update_data or "end_time" in update_data:
        overlapping = db.query(PersonalSchedule).filter(
            PersonalSchedule.user_id == current_user.id,
            PersonalSchedule.id != id,
            PersonalSchedule.scheduled_date == new_day,
            PersonalSchedule.start_time < new_end,
            PersonalSchedule.end_time > new_start
        ).first()

        if overlapping:
            raise HTTPException(status_code=409)

    for key, value in update_data.items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule



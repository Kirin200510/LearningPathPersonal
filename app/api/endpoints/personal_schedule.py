from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_active_user
from app.db.base import PathStatus
from app.model.learning_path import PathNode,LearningPath
from app.model.personal_schedule import PersonalSchedule
from app.model.course import Course
from app.schemas.personal_schedule import ScheduleCreate, ScheduleResponse,ScheduleUpdate
from app.model.user import User

router = APIRouter()

@router.get("/schedules/")
def get_schedules(db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user))->List[ScheduleResponse]:
    schedules=db.query(PersonalSchedule).filter(PersonalSchedule.user_id == current_user.id).all()
    return schedules

@router.post("/schedules/")
def create_user_schedule(data:ScheduleCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user))->List[ScheduleResponse]:
    if data.start_time >= data.end_time:
        raise HTTPException(status_code=400)

    node = db.query(PathNode).join(LearningPath).filter(
        LearningPath.user_id == current_user.id,
        LearningPath.status == PathStatus.ACTIVE,
        PathNode.course_id == data.course_id
    ).first()

    if not node or not node.is_unlocked:
        raise HTTPException(status_code=403)

    created_schedules=[]

    for day in data.days_of_week:
        #check trùng lịch
        overlapping=db.query(PersonalSchedule).filter(
            PersonalSchedule.user_id == current_user.id,
            PersonalSchedule.day_of_week == day,
            PersonalSchedule.start_time < data.end_time,
            PersonalSchedule.end_time > data.start_time
        ).first()
        if overlapping:
            raise HTTPException(status_code=409)

        new_schedule = PersonalSchedule(
            user_id=current_user.id,
            course_id=data.course_id,
            day_of_week=day,
            start_time=data.start_time,
            end_time=data.end_time,
            is_reminder_enabled=data.is_reminder_enabled
        )
        created_schedules.append(new_schedule)

    db.add_all(created_schedules)
    db.commit()
    for schedule in created_schedules:
        db.refresh(schedule)

    return created_schedules

@router.patch("/schedules/{id}/")
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

    new_day = update_data.get("day_of_week", schedule.day_of_week)
    new_start = update_data.get("start_time", schedule.start_time)
    new_end = update_data.get("end_time", schedule.end_time)

    if new_start >= new_end:
        raise HTTPException(status_code=400)

    if "day_of_week" in update_data or "start_time" in update_data or "end_time" in update_data:
        overlapping = db.query(PersonalSchedule).filter(
            PersonalSchedule.user_id == current_user.id,
            PersonalSchedule.id != id,
            PersonalSchedule.day_of_week == new_day,
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

@router.delete("/schedules/{id}")
def delete_user_schedule(id:int,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    schedule = db.query(PersonalSchedule).filter(
        PersonalSchedule.id == id,
        PersonalSchedule.user_id == current_user.id
    ).first()

    if not schedule:
        raise HTTPException(status_code=404)
    db.delete(schedule)
    db.commit()
    return {"detail": "Xóa thành công"}



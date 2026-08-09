from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db, get_current_active_user
from app.core.security import get_password_hash,verify_password
from app.model.skill import UserSkill, Skill
from app.schemas.skill import UserSkillResponse,UserSkillCreate,UserSkillUpdate
from app.schemas.user import UserCreate, UserResponse, UserUpdate, ChangePassword
from app.model.user import User

router = APIRouter()

@router.post("/")
def register_user(user:UserCreate,db:Session=Depends(get_db))->UserResponse:
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=404, detail="User already exists")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        avatar=user.avatar
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("users/me/")
def profile(current_user:User = Depends(get_current_active_user))->UserResponse:
    return current_user

@router.patch("users/me/")
def update_user(update_user:UserUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user))->UserResponse:
    # Khong trung username
    if update_user.username and update_user.username != current_user.username:
        user_exists = db.query(User).filter(User.username == update_user.username).first()
        if user_exists:
            raise HTTPException(status_code=400,detail="User already exists")

    update_data = update_user.model_dump(exclude_unset=True)# bỏ qua các trường bị trống

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("users/me/change-password/")
def change_password(pwd_data: ChangePassword,current_user:User = Depends(get_current_active_user),db: Session = Depends(get_db),)->UserResponse:
    if not verify_password(pwd_data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400,detail="Invalid password")

    if pwd_data.new_password == pwd_data.old_password:
        raise HTTPException(status_code=400)

    hashed_password = get_password_hash(pwd_data.new_password)
    current_user.password_hash = hashed_password

    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me/skills/")
def get_known_skills(current_user:User = Depends(get_current_active_user),db: Session = Depends(get_db))->List[UserSkillResponse]:
    known_skills=db.query(UserSkill).options(joinedload(UserSkill.skill)).filter(UserSkill.user_id == current_user.id).all()
    return known_skills

@router.post("/me/skills/")
def add_known_skill(data:UserSkillCreate,db:Session = Depends(get_db),current_user:User = Depends(get_current_active_user))->UserSkillResponse:
    skill = db.query(Skill).filter(Skill.id == data.skill_id).first()
    if not skill:
        raise HTTPException(status_code=400,detail="Skill not found")

    exist_skill=(db.query(UserSkill).filter(UserSkill.user_id == current_user.id,
                                           UserSkill.skill_id==data.skill_id)
                 .first())
    if exist_skill:
        raise HTTPException(status_code=409,detail="User already has this skill")

    user_skill = UserSkill(user_id=current_user.id,skill_id=data.skill_id,proficiency_level=data.proficiency_level)
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)
    return user_skill

@router.patch("/me/skills/{skill_id}/")
def update_known_skill(skill_id:int,data:UserSkillUpdate,db:Session = Depends(get_db),current_user:User = Depends(get_current_active_user))->UserSkillResponse:
    user_skill = db.query(UserSkill).filter(UserSkill.skill_id == skill_id,UserSkill.user_id==current_user.id).first()
    if not user_skill:
        raise HTTPException(status_code=404,detail="Known skill not found")
    user_skill.proficiency_level = data.proficiency_level

    db.commit()
    db.refresh(user_skill)
    return user_skill

@router.delete("/me/skills/{skill_id}/")
def delete_known_skill(skill_id:int,db:Session = Depends(get_db),current_user:User = Depends(get_current_active_user)):
    user_skill = db.query(UserSkill).filter(UserSkill.skill_id == skill_id,
                                            UserSkill.user_id == current_user.id).first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="Known skill not found")
    db.delete(user_skill)
    db.commit()
    return { "detail":"Xóa thành công"}

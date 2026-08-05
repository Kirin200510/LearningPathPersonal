from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.core.security import get_password_hash,verify_password
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

@router.get("/me/")
def profile(current_user:User = Depends(get_current_active_user))->UserResponse:
    return current_user

@router.patch("/me/")
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

@router.post("/me/change-password/")
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
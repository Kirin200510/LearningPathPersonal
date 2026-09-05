from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.security import oauth2_scheme, verify_access_token
from app.model.learning_path import LearningPath
from app.model.user import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    token_data=verify_access_token(token)
    user=db.query(User).filter(User.username==token_data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User does not exist',headers={"WWW-Authenticate": "Bearer"})
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=404,detail='Inactive user')
    return current_user

def get_valid_learning_path(id: int,db: Session = Depends(get_db),current_user:User = Depends(get_current_user))->LearningPath:
    path=db.query(LearningPath).filter(LearningPath.id == id).first()

    if path is None:
        raise HTTPException(status_code=404,detail='Learning path does not exist')
    if path.user_id != current_user.id:
        raise HTTPException(status_code=403,detail='Do not have permission to access this resource')
    return path







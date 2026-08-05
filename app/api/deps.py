from fastapi import Depends, HTTPException, status
import jwt # (Tùy thuộc bạn cài thư viện PyJWT hay python-jose)
from sqlalchemy.orm import Session

from app.db.base import ProgressStatus, PathStatus
from app.db.session import SessionLocal
from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.model.course import Course
from app.model.learning_path import LearningPath, PathNode
from app.model.user import User
from app.model.lesson import Lesson, LessonProgress
from app.schemas.learning_path import LearningPathResponse
from app.schemas.user import TokenData
from app.core.security import verify_access_token

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

def get_valid_learning_path(id: int,db: Session = Depends(get_db),current_user:User = Depends(get_current_user))->LearningPathResponse:
    path=db.query(LearningPath).filter(LearningPath.id == id).first()

    if path is None:
        raise HTTPException(status_code=404,detail='Learning path does not exist')
    if path.user_id != current_user.id:
        raise HTTPException(status_code=403,detail='Do not have permission to access this resource')
    return path

def get_valid_lesson_for_user(id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user))->Lesson:
    lesson = db.query(Lesson).filter(Lesson.id == id).first()
    if lesson is None:
        raise HTTPException(status_code=404,detail='Lesson does not exist')
    node = db.query(PathNode).join(LearningPath).filter(
        LearningPath.user_id == current_user.id,
        PathNode.course_id == lesson.course_id,
        LearningPath.status == "ACTIVE").first()
    # Lesson do khong trong lo trinh
    if not node:
        raise HTTPException(status_code=403)
    if not node.is_unlocked:
        raise HTTPException(status_code=403,detail='You cannot unlock the course and lessons')
    return lesson

def check_and_unlock_next_course(db: Session, user_id: int, course_id: int) -> bool:
   lesson_total=db.query(Lesson).filter(Lesson.course_id==course_id).count()
   if lesson_total==0:
       return False

   completed_lesson=(db.query(LessonProgress)
                     .join(Lesson)
                     .filter(LessonProgress.user_id == user_id,
                             LessonProgress.lesson_id==Lesson.id,
                             LessonProgress.status == ProgressStatus.COMPLETED).count())
   if completed_lesson < lesson_total:
       return False
   #current_course
   current_node = (
       db.query(PathNode)
       .join(LearningPath)
       .filter(
           LearningPath.user_id == user_id,
           PathNode.course_id == course_id,
           LearningPath.status == PathStatus.ACTIVE
       ).first())

   if current_node is None or current_node.status == ProgressStatus.COMPLETED:
       return False

   current_node.status = ProgressStatus.COMPLETED

   #find next node(next course in path)
   next_node=(db.query(PathNode).
              filter(PathNode.learning_path_id==current_node.learning_path_id,
                     PathNode.sequence_order==current_node.sequence_order+1)
              .first())
   if next_node:
       next_node.is_unlocked = True
       next_node.status = ProgressStatus.IN_PROGRESS
       return True
   # no node next
   return False





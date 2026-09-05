from fastapi import APIRouter, Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_valid_learning_path
from app.model.learning_path import LearningPath, PathNode
from app.model.user import User
from app.schemas.learning_path import LearningPathResponse, PathNodeResponse

from app.api.deps import get_current_active_user
from app.model.personal_schedule import PersonalSchedule

router = APIRouter()



@router.get("/learning_path/me/")
def get_learning_paths(current_user: User = Depends(get_current_active_user),db: Session = Depends(get_db))->List[LearningPathResponse]:
    paths = db.query(LearningPath).filter(LearningPath.user_id == current_user.id).order_by(LearningPath.created_at.desc()).all()
    return paths

@router.get("/learning_path/{id}/nodes/")
def get_learning_path_nodes(path: LearningPath=Depends(get_valid_learning_path))->List[PathNodeResponse]:
    return path.nodes

@router.delete("/learning_path/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_learning_path(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    path = db.query(LearningPath).filter(LearningPath.id == id,LearningPath.user_id == current_user.id).first()
    if not path:
        raise HTTPException(tatus_code=404)

    try:
        # Xóa lịch thuộc lộ trình
        db.query(PersonalSchedule).filter(
            PersonalSchedule.learning_path_id == id,
            PersonalSchedule.user_id == current_user.id
        ).delete()

        # Xóa các node của lộ trình
        db.query(PathNode).filter(
            PathNode.learning_path_id == id
        ).delete()

        # Xóa LearningPath
        db.delete(path)

        db.commit()

    except Exception:
        db.rollback()
        raise

    return Response(status_code=status.HTTP_204_NO_CONTENT)


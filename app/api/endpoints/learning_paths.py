from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user, get_valid_learning_path
from app.model.learning_path import LearningPath, PathNode
from app.model.user import User
from app.schemas.learning_path import LearningPathCreate, LearningPathResponse, PathNodeResponse

router = APIRouter()

@router.post("/learning_path/")
def create_learning_path(data:LearningPathCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user))->LearningPathResponse:
    if not data.course_ids:
        raise HTTPException(status_code=400, detail="Courses are required")

    new_path = LearningPath(user_id=current_user.id, career_goal_id=data.career_goal_id)
    db.add(new_path)
    db.flush()
    list_nodes=[]
    for index,course_id in enumerate(data.course_ids):
        if index == 0:
            is_first_course = True
        else:
            is_first_course = False
        node=PathNode(learning_path_id=new_path.id,course_id=course_id,sequence_order=index+1)
        list_nodes.append(node)

    db.add_all(list_nodes)
    db.commit()
    db.refresh(new_path)

    return new_path

@router.get("/learning_path/me/")
def get_learning_paths(current_user: User = Depends(get_current_user),db: Session = Depends(get_db))->List[LearningPathResponse]:
    paths = db.query(LearningPath).filter(LearningPath.user_id == current_user.id).order_by(LearningPath.created_at.desc()).all()
    return paths

@router.get("/learning_path/{id}/nodes/")
def get_learning_path_nodes(path: LearningPath=Depends(get_valid_learning_path))->List[PathNodeResponse]:
    return path.nodes


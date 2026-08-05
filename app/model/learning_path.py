from sqlalchemy import Column,Integer,String,ForeignKey,Enum,DateTime,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base,ProgressStatus,PathStatus
from datetime import datetime

class LearningPath(Base):
    __tablename__ = "learning_path"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    career_goal_id = Column(Integer, ForeignKey("career_goal.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(PathStatus), default=PathStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.now)

    users = relationship("User", back_populates="learning_paths")
    nodes = relationship("PathNode", back_populates="learning_paths", order_by="PathNode.sequence_order")

class PathNode(Base):
    __tablename__ = "path_node"

    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_path.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))
    sequence_order = Column(Integer, nullable=False)
    is_unlocked = Column(Boolean, default=False)
    status = Column(Enum(ProgressStatus), default=ProgressStatus.TODO)

    learning_paths = relationship("LearningPath", back_populates="nodes")
    courses = relationship("Course")

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class LearningPath(Base):
    __tablename__ = "learning_path"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    career_goal_id = Column(Integer, ForeignKey("career_goal.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    nodes = relationship("PathNode",order_by="PathNode.sequence_order",cascade="all, delete-orphan")

class PathNode(Base):
    __tablename__ = "path_node"

    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_path.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))
    sequence_order = Column(Integer, nullable=False)


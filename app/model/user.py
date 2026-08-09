from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False,unique=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    avatar = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)

    #Relationship
    learning_paths = relationship("LearningPath", cascade="all, delete-orphan")
    schedules = relationship("PersonalSchedule",cascade="all, delete-orphan")
    known_skills = relationship(    "UserSkill", cascade="all, delete-orphan")
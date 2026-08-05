from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Boolean, Time
from sqlalchemy.orm import relationship
from app.db.base import Base,ProgressStatus,PathStatus
from datetime import datetime

class PersonalSchedule(Base):
    __tablename__ = "personal_schedule"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))
    day_of_week = Column(Integer, nullable=False) # 2 đến 8
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_reminder_enabled = Column(Boolean, default=True)

    users = relationship("User", back_populates="schedules")
    courses = relationship("Course")
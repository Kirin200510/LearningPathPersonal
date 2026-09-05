from sqlalchemy import Column, Integer, ForeignKey, Boolean, Time,Date
from app.db.base import Base

class PersonalSchedule(Base):
    __tablename__ = "personal_schedule"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))
    scheduled_date = Column(Date,nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_reminder_enabled = Column(Boolean, default=True)

    learning_path_id = Column(Integer,ForeignKey("learning_path.id", ondelete="CASCADE"),nullable=False)

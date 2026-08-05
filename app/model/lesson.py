from sqlalchemy import Column,Integer,String,ForeignKey,Enum,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base,ProgressStatus

class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))
    title = Column(String(100), nullable=False)
    content_type = Column(String(200)) # Video, Reading, Quiz...
    content_url = Column(String(300), nullable=True)
    duration_seconds = Column(Integer, default=0)
    sequence_order = Column(Integer, nullable=False, default=1)

    courses = relationship("Course", back_populates="lessons")
    progresses = relationship("LessonProgress", back_populates="lessons")


class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    lesson_id = Column(Integer, ForeignKey("lesson.id", ondelete="CASCADE"))
    status = Column(Enum(ProgressStatus), default=ProgressStatus.TODO)

    watched_seconds = Column(Integer, default=0)  # Số giây thực tế đã xem để tính %

    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    users = relationship("User", back_populates="lesson_progresses")
    lessons = relationship("Lesson", back_populates="progresses")
from sqlalchemy import Column,Integer,String,ForeignKey,Text
from sqlalchemy.orm import relationship

from app.db.base import Base

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    estimated_hours = Column(Integer, nullable=True)

    skills = relationship("CourseSkill", back_populates="courses")

#Khóa học tiên quyết
class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))
    prerequisite_course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"))

class CourseSkill(Base):
    __tablename__ = "course_skills"

    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"),primary_key=True)
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"),primary_key=True)

    courses = relationship("Course", back_populates="skills")
    skills = relationship("Skill",back_populates="courses")
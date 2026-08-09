from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Skill(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    courses = relationship("CourseSkill", back_populates="skills")
    career_goals = relationship("GoalSkill", back_populates="skills")

class GoalSkill(Base):
    __tablename__ = "goal_skill"

    goal_id = Column(Integer, ForeignKey("career_goal.id", ondelete="CASCADE"),primary_key=True)
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"),primary_key=True)
    weight = Column(Integer, default=1)

    career_goals = relationship("CareerGoal", back_populates="skills")
    skills = relationship("Skill", back_populates="career_goals")


class UserSkill(Base):
    __tablename__ = "user_skill"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"))

    # Đánh giá mức độ tự tin với kỹ năng này (1 đến 5 sao)
    proficiency_level = Column(Integer, default=3)


    skill = relationship("Skill")
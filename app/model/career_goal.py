from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import relationship

from app.db.base import Base
# Mục tiêu nghề nghiệp
class CareerGoal(Base):
    __tablename__ = "career_goal"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    skills = relationship("GoalSkill", back_populates="career_goals")


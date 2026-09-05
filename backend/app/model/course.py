from sqlalchemy import Column,Integer,String,ForeignKey,Text
from sqlalchemy.orm import relationship

from app.db.base import Base

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(255),unique=True,nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    url=Column(Text,nullable=True)


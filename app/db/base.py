from sqlalchemy.orm import declarative_base
from  enum import Enum

Base=declarative_base()

class PathStatus(str, Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"

class ProgressStatus(str, Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


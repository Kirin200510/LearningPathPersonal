from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URI: str = 'mysql+pymysql://root:hod2t123@localhost:3306/learningpathdb'

settings = Settings()

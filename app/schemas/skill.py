from pydantic import BaseModel

class SkillBase(BaseModel):
    name: str

class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True
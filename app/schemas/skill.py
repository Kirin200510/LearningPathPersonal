from pydantic import BaseModel,Field

class SkillBase(BaseModel):
    name: str

class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True

class UserSkillCreate(BaseModel):
    skill_id: int
    proficiency_level: int = Field(ge=1,le=5 )


class UserSkillUpdate(BaseModel):
    proficiency_level: int = Field(ge=1,le=5)


class UserSkillResponse(BaseModel):
    id: int
    skill_id: int
    proficiency_level: int
    skill: SkillResponse

    class Config:
        from_attributes = True
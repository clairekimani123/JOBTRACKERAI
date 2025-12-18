from pydantic import BaseModel
from datetime import datetime


class AIMatchCreate(BaseModel):
    application_id: int
    resume_id: int


class AIMatchOut(BaseModel):
    id: int
    user_id: int
    application_id: int
    resume_id: int
    match_score: int
    strengths: str | None
    missing_skills: str | None
    recommendation: str | None
    created_at: datetime

    class Config:
        from_attributes = True

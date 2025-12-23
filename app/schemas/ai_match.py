from pydantic import BaseModel
from datetime import datetime
from typing import List


class AIMatchCreate(BaseModel):
    application_id: int
    resume_id: int


class AIMatchOut(BaseModel):
    id: int
    application_id: int
    resume_id: int
    match_score: int
    strengths: List[str]
    missing_skills: List[str]
    recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True

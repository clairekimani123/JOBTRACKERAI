from datetime import datetime
from pydantic import BaseModel

class ResumeBase(BaseModel):
    original_filename: str

class ResumeCreate(ResumeBase):
    pass

class ResumeOut(ResumeBase):
    id: int
    file_path: str
    extracted_text: str | None
    uploaded_at: datetime

    class Config:
        from_attributes = True

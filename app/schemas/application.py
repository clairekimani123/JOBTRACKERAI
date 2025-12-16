from datetime import date, datetime
from pydantic import BaseModel
from app.models.application import ApplicationStatus

# Shared fields
class ApplicationBase(BaseModel):
    company_name: str
    position_title: str
    job_description: str | None = None
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_date: date
    follow_up_date: date | None = None
    notes: str | None = None
    job_url: str | None = None
    salary_range: str | None = None
    location: str | None = None

# For creating an application
class ApplicationCreate(ApplicationBase):
    pass

# For updating an application (all optional)
class ApplicationUpdate(BaseModel):
    company_name: str | None = None
    position_title: str | None = None
    job_description: str | None = None
    status: ApplicationStatus | None = None
    applied_date: date | None = None
    follow_up_date: date | None = None
    notes: str | None = None
    job_url: str | None = None
    salary_range: str | None = None
    location: str | None = None

# Response schema
class ApplicationOut(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

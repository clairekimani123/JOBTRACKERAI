from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

# Enum for application status
class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class Application(Base):
    __tablename__ = "applications"
    
    # Primary Key - MUST HAVE THIS!
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key (links to User table)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Application fields
    company_name = Column(String, nullable=False)
    position_title = Column(String, nullable=False)
    job_description = Column(Text, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_date = Column(Date, nullable=False)
    follow_up_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    job_url = Column(String, nullable=True)
    salary_range = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship (connects back to User)
    user = relationship("User", back_populates="applications")
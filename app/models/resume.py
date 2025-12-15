from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    # Primary Key - MUST HAVE THIS!
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key (links to User table)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Resume fields
    file_path = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship (connects back to User)
    user = relationship("User", back_populates="resumes")



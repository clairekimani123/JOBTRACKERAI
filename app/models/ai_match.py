from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class AIMatch(Base):
    __tablename__ = "ai_matches"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)

    match_score = Column(Integer, nullable=False)
    strengths = Column(Text)
    missing_skills = Column(Text)
    recommendation = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    application = relationship("Application")
    resume = relationship("Resume")

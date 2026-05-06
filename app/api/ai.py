import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.ai_match import AIMatchCreate, AIMatchOut
from app.models.application import Application
from app.models.resume import Resume
from app.models.ai_match import AIMatch
from app.services.ai_service import run_resume_match

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/match", response_model=AIMatchOut)
def ai_match(
    payload: AIMatchCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    application = (
        db.query(Application)
        .filter(Application.id == payload.application_id,
                Application.user_id == user.id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    resume = (
        db.query(Resume)
        .filter(Resume.id == payload.resume_id,
                Resume.user_id == user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if not resume.extracted_text or len(resume.extracted_text) < 100:
        raise HTTPException(status_code=400, detail="Resume text extraction failed or is too short")

    if not application.job_description:
        raise HTTPException(status_code=400, detail="Job description is required for matching")

    ai_result = run_resume_match(
        resume_text=resume.extracted_text,
        job_description=application.job_description
    )

    match = AIMatch(
        user_id=user.id,
        application_id=application.id,
        resume_id=resume.id,
        match_score=ai_result["match_score"],
        strengths=ai_result["strengths"],
        missing_skills=ai_result["missing_skills"],
        recommendation=ai_result["recommendation"],
    )
    db.add(match)
    db.commit()
    db.refresh(match)

    return {
        "id": match.id,
        "application_id": match.application_id,
        "resume_id": match.resume_id,
        "match_score": match.match_score,
        "strengths": match.strengths,
        "missing_skills": match.missing_skills,
        "recommendation": match.recommendation,
        "created_at": match.created_at,
    }

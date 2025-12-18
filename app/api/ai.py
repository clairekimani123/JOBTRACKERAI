from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.application import Application
from app.models.resume import Resume
from app.models.ai_match import AIMatch
from app.schemas.ai import AIMatchCreate, AIMatchOut
from app.services.matcher_ai import ai_match_resume

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)

# -------------------------------
# 1️⃣ CREATE AI MATCH (SAVE RESULT)
# -------------------------------
@router.post("/match", response_model=AIMatchOut)
def run_ai_match(
    payload: AIMatchCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == payload.application_id,
        Application.user_id == user.id
    ).first()

    resume = db.query(Resume).filter(
        Resume.id == payload.resume_id,
        Resume.user_id == user.id
    ).first()

    if not application or not resume:
        raise HTTPException(status_code=404, detail="Application or Resume not found")

    ai_result = ai_match_resume(
        resume_text=resume.extracted_text or "",
        job_description=application.job_description or ""
    )

    ai_match = AIMatch(
        user_id=user.id,
        application_id=application.id,
        resume_id=resume.id,
        match_score=ai_result["match_score"],
        strengths=", ".join(ai_result["strengths"]),
        missing_skills=", ".join(ai_result["missing_skills"]),
        recommendation=ai_result["recommendation"]
    )

    db.add(ai_match)
    db.commit()
    db.refresh(ai_match)

    return ai_match


# -------------------------------
# 2️⃣ AI MATCH HISTORY
# -------------------------------
@router.get("/history", response_model=list[AIMatchOut])
def ai_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return (
        db.query(AIMatch)
        .filter(AIMatch.user_id == user.id)
        .order_by(AIMatch.created_at.desc())
        .all()
    )


# -------------------------------
# 3️⃣ AI RANKINGS
# -------------------------------
@router.get("/rankings")
def ai_ranked_applications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    results = (
        db.query(AIMatch)
        .filter(AIMatch.user_id == user.id)
        .order_by(AIMatch.match_score.desc())
        .all()
    )

    return [
        {
            "application_id": r.application_id,
            "resume_id": r.resume_id,
            "match_score": r.match_score,
            "recommendation": r.recommendation
        }
        for r in results
    ]

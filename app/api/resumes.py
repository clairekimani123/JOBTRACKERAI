import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.resume import Resume
from app.schemas.resume import ResumeOut

UPLOAD_DIR = "uploads/resumes"

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)

os.makedirs(UPLOAD_DIR, exist_ok=True)


# UPLOAD RESUME
@router.post("/upload", response_model=ResumeOut, status_code=status.HTTP_201_CREATED)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_id = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    resume = Resume(
        user_id=user.id,
        file_path=file_path,
        original_filename=file.filename
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


# LIST USER RESUMES
@router.get("/", response_model=list[ResumeOut])
def list_resumes(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Resume).filter(
        Resume.user_id == user.id
    ).order_by(Resume.uploaded_at.desc()).all()


# GET SINGLE RESUME
@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return resume


# DELETE RESUME
@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    db.delete(resume)
    db.commit()

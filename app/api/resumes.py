import os

import uuid

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from sqlalchemy.orm import Session



from app.core.database import get_db

from app.core.deps import get_current_user

from app.models.resume import Resume

from app.schemas.resume import ResumeOut

from app.services.pdf_service import extract_text_from_pdf



router = APIRouter(prefix="/resumes", tags=["Resumes"])



UPLOAD_DIR = "uploads/resumes"

os.makedirs(UPLOAD_DIR, exist_ok=True)





@router.post("/upload", response_model=ResumeOut)

def upload_resume(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    user=Depends(get_current_user)

):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(status_code=400, detail="Only PDF files are allowed")



    # 1️⃣ Save file

    ext = file.filename.split(".")[-1]

    unique_filename = f"{uuid.uuid4()}.{ext}"

    file_path = os.path.join(UPLOAD_DIR, unique_filename)



    with open(file_path, "wb") as f:

        f.write(file.file.read())



    # 2️⃣ Extract text from PDF

    extracted_text = extract_text_from_pdf(file_path)



    # 3️⃣ Save to DB

    resume = Resume(

        user_id=user.id,

        original_filename=file.filename,

        file_path=file_path,

        extracted_text=extracted_text

    )



    db.add(resume)

    db.commit()

    db.refresh(resume)



    return resume





@router.get("/", response_model=list[ResumeOut])

def list_resumes(

    db: Session = Depends(get_db),

    user=Depends(get_current_user)

):

    return (

        db.query(Resume)

        .filter(Resume.user_id == user.id)

        .order_by(Resume.uploaded_at.desc())

        .all()

    )





@router.get("/{resume_id}", response_model=ResumeOut)

def get_resume(

    resume_id: int,

    db: Session = Depends(get_db),

    user=Depends(get_current_user)

):

    resume = (

        db.query(Resume)

        .filter(Resume.id == resume_id, Resume.user_id == user.id)

        .first()

    )



    if not resume:

        raise HTTPException(status_code=404, detail="Resume not found")



    return resume





@router.delete("/{resume_id}", status_code=204)

def delete_resume(

    resume_id: int,

    db: Session = Depends(get_db),

    user=Depends(get_current_user)

):

    resume = (

        db.query(Resume)

        .filter(Resume.id == resume_id, Resume.user_id == user.id)

        .first()

    )



    if not resume:

        raise HTTPException(status_code=404, detail="Resume not found")



    db.delete(resume)

    db.commit()


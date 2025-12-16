from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.application import Application, ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationOut
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

# CREATE
@router.post("/", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    application = Application(
        **data.dict(),
        user_id=user.id
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


# LIST (user-specific)
@router.get("/", response_model=list[ApplicationOut])
def list_applications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return (
        db.query(Application)
        .filter(Application.user_id == user.id)
        .order_by(Application.created_at.desc())
        .all()
    )


# GET SINGLE
@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user.id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


# UPDATE (PARTIAL)
@router.put("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user.id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


# DELETE
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user.id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()


# DASHBOARD STATS
@router.get("/stats/summary")
def application_stats(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    total = db.query(func.count(Application.id)).filter(
        Application.user_id == user.id
    ).scalar()

    by_status = (
        db.query(Application.status, func.count(Application.id))
        .filter(Application.user_id == user.id)
        .group_by(Application.status)
        .all()
    )

    return {
        "total": total,
        "by_status": {status.value: count for status, count in by_status}
    }

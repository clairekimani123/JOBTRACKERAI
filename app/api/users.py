from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.user import UserOut

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# CURRENT USER PROFILE
@router.get("/me", response_model=UserOut)
def get_me(
    user=Depends(get_current_user)
):
    return user

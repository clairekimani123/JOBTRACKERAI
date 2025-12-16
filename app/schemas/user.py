from datetime import datetime
from pydantic import BaseModel, EmailStr

# Base
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

# For registration
class UserCreate(UserBase):
    password: str

# For responses
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

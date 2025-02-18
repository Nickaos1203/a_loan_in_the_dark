from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_staff: bool

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    is_staff: bool
    is_active: bool
    first_connection: bool
    profile_picture: Optional[str]

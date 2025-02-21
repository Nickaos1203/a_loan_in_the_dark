from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CONSEILLER = "conseiller"
    CLIENT = "client"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.CLIENT)
    is_active: bool = Field(default=False)
    activation_token: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")

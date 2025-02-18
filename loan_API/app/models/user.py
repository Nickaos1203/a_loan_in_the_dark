from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import uuid4, UUID
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=False)
    first_connection: bool = Field(default=True)
    profile_picture: Optional[str] = Field(default=None)

    def verify_password(self, password: str) -> bool:
        """Vérifie si le mot de passe fourni correspond au hash stocké"""
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash un mot de passe avec bcrypt"""
        return pwd_context.hash(password)

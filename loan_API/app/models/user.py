from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import uuid4, UUID
import bcrypt

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(
        sa_column=Column("email", String(255), nullable=False, unique=True, index=True)
    )
    hashed_password: str = Field(
        sa_column=Column("hashed_password", String(255), nullable=False)
    )
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=False)
    first_connection: bool = Field(default=True)
    first_name: Optional[str] = Field(
        default=None, sa_column=Column("first_name", String(100))
    )
    last_name: Optional[str] = Field(
        default=None, sa_column=Column("last_name", String(100))
    )
    username: Optional[str] = Field(
        default=None, sa_column=Column("username", String(100))
    )
    phone_number: Optional[str] = Field(
        default=None, sa_column=Column("phone_number", String(20))
    )
    
    # Relation one-to-many
    advisor_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    advisor: Optional["User"] = Relationship(
        back_populates="users", 
        sa_relationship_kwargs={"remote_side": "User.id"}
    )
    
    # Liste des users rattachés au conseiller
    users: List["User"] = Relationship(back_populates="advisor")
    
    

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the stored hashed password.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a given password using bcrypt.

        Args:
            password (str): The plaintext password to hash.

        Returns:
            str: The hashed password as a string.
        """
        salt = bcrypt.gensalt()  # Generate a salt for hashing
        hashed = bcrypt.hashpw(password.encode(), salt)  # Hash the password
        return hashed.decode()  # Convert bytes to string
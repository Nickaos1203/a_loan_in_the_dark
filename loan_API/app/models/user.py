from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import uuid4, UUID
import bcrypt
from app.models.loan import Loan

class User(SQLModel, table=True):
    """
    Represents a user in the system.

    Attributes:
        id (UUID): Unique identifier for the user, generated automatically.
        email (str): User's email address, must be unique.
        hashed_password (str): Hashed version of the user's password.
        is_staff (bool): Indicates if the user has administrative privileges.
        is_active (bool): Defines if the user's account is currently active.
        first_connection (bool): Specifies if the user is logging in for the first time.
        profile_picture (Optional[str]): URL or path to the user's profile picture.
    """
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=False)
    first_connection: bool = Field(default=True)
    profile_picture: Optional[str] = Field(default=None)
    loan: Optional["Loan"] = Relationship(back_populates="user", uselist=False)

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
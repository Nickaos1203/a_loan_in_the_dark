from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from app.models.user import User

class UserCreate(BaseModel):
    """
    Schema for user creation.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The plain text password to be hashed later.
        is_staff (bool): Defines if the user has administrative privileges.
    """
    email: EmailStr
    password: str
    is_staff: bool

class UserConnection(BaseModel):
    """
    Schema for user authentication (login).

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The plain text password for authentication.
    """
    email: EmailStr
    password: str

class UserRead(BaseModel):
    """
    Schema for reading user information.

    Attributes:
        id (UUID): The unique identifier of the user.
        email (EmailStr): The email address of the user.
        is_staff (bool): Indicates if the user has administrative privileges.
        is_active (bool): Indicates if the user's account is active.
        first_connection (bool): Specifies whether it is the user's first login.
        profile_picture (Optional[str]): URL or path to the user's profile picture.
    """
    id: UUID
    email: EmailStr
    is_staff: bool
    is_active: bool
    first_connection: bool
    profile_picture: Optional[str]
    # add properties : first_name, last_name, phone_number
    first_name: str
    last_name: str
    phone_number: str
    advisor_id: UUID


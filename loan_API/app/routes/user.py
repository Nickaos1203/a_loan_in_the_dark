from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user, get_user_by_id, update_user
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/create_user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_create: UserCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new user. Only staff users can access this route.

    Args:
        user_create (UserCreate): The data of the user to be created.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        UserRead: The created user information.

    Raises:
        HTTPException: If the current user is not a staff member.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You must be a staff user.",
        )
    return create_user(db=db, user_create=user_create)

@router.get("/user/{user_id}", response_model=UserRead)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves a user by their ID.

    Args:
        user_id (UUID): The ID of the user.
        db (Session): The database session.

    Returns:
        UserRead: The retrieved user information.
    
    Raises:
        HTTPException: If the user is not found.
    """
    return get_user_by_id(db=db, user_id=user_id)

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Returns the currently authenticated user's basic details.

    Args:
        current_user (User): The authenticated user.

    Returns:
        dict: The user's ID and email.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
    }

@router.put("/me/edit")
def update_user_me(
    user_update: UserRead, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Update details about the current user.
    Args:
        user_update (User): The authentificated user with updated details
        db (Session): The database session.
        current_user (User): The currently authenticated user.
    """
    update_user(db,user_update)

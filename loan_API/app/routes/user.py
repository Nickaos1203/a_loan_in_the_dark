# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user, get_user_by_id
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_new_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """Crée un nouvel utilisateur"""
    return create_user(db=db, user_create=user_create)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """Récupère un utilisateur par son ID"""
    return get_user_by_id(db=db, user_id=user_id)

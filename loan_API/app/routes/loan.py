from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.loan import LoanCreate
from app.services.loan import create_loan
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()

@router.post("/create_loan", status_code=status.HTTP_201_CREATED)
def create_new_loan(loan_create: LoanCreate, db: Session = Depends(get_db)):
    return create_loan(db=db, loan_create=loan_create)
from app.models.user import User
from app.models.loan import Loan
from app.schemas.loan import LoanCreate
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

def create_loan(db: Session, loan_create: LoanCreate) -> None:
    user = db.query(User).filter(User.email == loan_create.user_email).first()
    # Check if loan already created
    db_loan = db.query(Loan).filter(Loan.user_id == user.id).first()
    if db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan already created",
        )
    
    # Create a new loan
    db_loan = Loan(
        user_id = user.id,
        user = user,
        state = loan_create.state,
        bank = loan_create.bank,
        naics = loan_create.naics,
        rev_line_cr = loan_create.rev_line_cr,
        low_doc = loan_create.low_doc,
        new_exist = loan_create.new_exist,
        create_job = loan_create.create_job,
        has_franchise= loan_create.has_franchise,
        recession=loan_create.recession,
        urban_rural=loan_create.urban_rural,
        term = loan_create.term,
        no_emp= loan_create.no_emp,
        gr_appv=loan_create.gr_appv
    )

    db_loan.make_prediction()
    
    # Save user to the database
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

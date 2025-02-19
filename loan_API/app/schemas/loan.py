from pydantic import BaseModel,  model_validator, EmailStr
from uuid import UUID
from typing import Optional
from app.models.loan import StateEnum, NAICSEnum, YesNoEnum

class LoanCreate(BaseModel):
    user_email: EmailStr

    state: StateEnum
    bank: str
    naics: NAICSEnum
    rev_line_cr: YesNoEnum
    low_doc: YesNoEnum
    
    new_exist: Optional[int]
    create_job: Optional[int]
    retained_job: Optional[int]
    has_franchise: Optional[int]
    recession: Optional[int]
    urban_rural: Optional[int]

    term: int
    no_emp: int
    gr_appv: float

    @model_validator(mode='before')
    def check_values(cls, values):
        # Validation des champs 0, 1, ou null
        for field in ['new_exist', 'has_franchise', 'recession', 'urban_rural']:
            val = values.get(field)
            if val is not None and val not in [0, 1]:
                raise ValueError(f"{field} must be either 0, 1, or null.")
        
        # Validation des valeurs numériques positives
        for field in ['term', 'no_emp', 'gr_appv', 'retained_job', 'create_job']:
            val = values.get(field)
            if val < 0:
                raise ValueError(f"{field} must be a positive number.")
        
        return values

    class Config:
        orm_mode = True
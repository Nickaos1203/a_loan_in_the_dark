# create_tables.py
from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.loan import Loan

def create_tables():
    SQLModel.metadata.create_all(engine)
    print("Tables créées avec succès")

if __name__ == "__main__":
    create_tables()
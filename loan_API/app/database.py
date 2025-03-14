from sqlmodel import create_engine, Session
import os 
from dotenv import load_dotenv

load_dotenv()

# Environnment variables
server = os.getenv("SERVER_DB")
database = os.getenv("DATABASE_NAME")
username = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD_DB")
driver = os.getenv("DRIVER_DB")

# Define the database URL
DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server"

# Create a database engine
engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    """
    Provides a database session for dependency injection.

    Yields:
        Session: A database session.
    """
    with Session(engine) as session:
        yield session

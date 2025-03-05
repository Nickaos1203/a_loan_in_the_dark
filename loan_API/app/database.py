from sqlmodel import create_engine, Session
import sqlmodel
import os
from dotenv import load_dotenv

load_dotenv()

# Utiliser les variables d'environnement pour la configuration
DB_SERVER = os.getenv("DB_SERVER", "lgallussqlserver.database.windows.net")
DB_NAME = os.getenv("DB_NAME", "bddussba")
DB_USER = os.getenv("DB_USER", "leo")
DB_PASSWORD = os.getenv("DB_PASSWORD", "leflibustierdu59!")

# Connexion à SQL Server
CONNECTION_STRING = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server"

# Create a database engine
engine = create_engine(CONNECTION_STRING, echo=True)

def get_db():
    """
    Provides a database session for dependency injection.
    """
    with Session(engine) as session:
        yield session
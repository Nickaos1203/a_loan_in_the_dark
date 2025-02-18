from sqlmodel import create_engine, Session


DATABASE_URL = "sqlite:///./app/db.sqlite3"
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_db():
    with Session(engine) as session:
        yield session

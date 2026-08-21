from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_PATH = (
    Path(__file__).resolve().parent / ".dapurkira.db"
)

DATABASE_URL = (
    f"sqlite:///{DATABASE_PATH.as_posix()}"
)

# Create the database connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for our future database tables
Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

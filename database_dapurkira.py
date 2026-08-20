from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Location and name of the SQLite database
DATABASE_URL = "sqlite:///.dapurkira.db"

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
"""
Database connection setup for Blood Test Analyzer API.

Currently unused, but ready for future features like:
- saving user analyses
- logging reports
- storing PDF metadata
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./blood_test_analyzer.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency for getting a DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from typing import Generator

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.settings import db_settings

import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5532")
DB_NAME = os.getenv("DB_NAME", "ai")
DB_USER = os.getenv("DB_USER", "ai")
DB_PASS = os.getenv("DB_PASS", "ai")

# Connection URL
db_url = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy Engine using a database URL
db_engine: Engine = create_engine(db_url, pool_pre_ping=True)

# Create a SessionLocal class
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-sessionlocal-class
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: An SQLAlchemy database session.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

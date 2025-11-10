from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

# Use PostgreSQL in production, SQLite in development
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create engine with appropriate config for SQLite vs PostgreSQL
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Get database session with proper error handling"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
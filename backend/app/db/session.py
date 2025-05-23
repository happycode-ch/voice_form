"""
File: backend/app/db/session.py
Description: SQLAlchemy database session management with centralized configuration.
AI-hints:
- Uses centralized config for DATABASE_URL
- Provides get_db() dependency for FastAPI
- Handles session lifecycle automatically
- Includes container startup retry logic for database connections
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import logging
from app.config import config
from sqlalchemy import text

logger = logging.getLogger(__name__)

def create_database_engine():
    """Create database engine with container-aware retry logic."""
    engine = create_engine(
        config.database_url,
        # Connection pool settings for containerized environment
        pool_pre_ping=True,      # Verify connections before use (handles container restarts)
        pool_recycle=300,        # Recycle connections after 5 minutes
        pool_timeout=20,         # Timeout for getting connection from pool
        pool_size=5,             # Number of connections to maintain
        max_overflow=10,         # Additional connections during peak load
        connect_args={
            "connect_timeout": 10  # Connection timeout for PostgreSQL
        }
    )
    return engine

def wait_for_database(engine, max_retries: int = None, retry_delay: int = None):
    """
    Wait for database to be available during container startup.
    
    Args:
        engine: SQLAlchemy engine
        max_retries: Maximum number of retry attempts (from config if None)
        retry_delay: Delay between retries in seconds (from config if None)
        
    Raises:
        Exception: If database is not available after all retries
    """
    if max_retries is None:
        max_retries = config.database_connection_retries
    if retry_delay is None:
        retry_delay = config.database_retry_delay_seconds
    
    logger.info(f"Waiting for database connection (max {max_retries} retries)...")
    
    for attempt in range(max_retries):
        try:
            # Test database connection - use text() for modern SQLAlchemy
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            return
            
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"❌ Database connection failed after {max_retries} attempts")
                raise Exception(f"Could not connect to database after {max_retries} attempts: {e}")

# Create SQLAlchemy engine using centralized configuration
engine = create_database_engine()

# Wait for database during module import (container startup)
try:
    wait_for_database(engine)
except Exception as e:
    logger.error(f"Failed to establish database connection during startup: {e}")
    # Don't raise here - let the application start and handle via health checks
    # This allows the container to start even if DB is temporarily unavailable

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    """
    Database session dependency with container-aware error handling.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close() 
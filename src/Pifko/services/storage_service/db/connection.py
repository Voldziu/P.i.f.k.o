import os
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager


# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pifko_user:pifko_password123@localhost:5432/brewery_storage",
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    """Context manager for database session"""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

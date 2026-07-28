"""
Database client for the Vector Database module.
"""

from sqlalchemy.orm import Session

from .database import SessionLocal


class VectorDBClient:
    """
    Provides a simple interface for obtaining
    and closing database sessions.
    """

    def __init__(self):
        self.db: Session = SessionLocal()

    def get_session(self) -> Session:
        """
        Returns the active database session.
        """
        return self.db

    def close(self):
        """
        Closes the database session.
        """
        self.db.close()
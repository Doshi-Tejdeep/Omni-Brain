"""
Database migration utility.

Creates all database tables defined in models.py.
"""

from .database import Base, engine

# Import models so SQLAlchemy registers them
from .models import Document, History


def run_migration():
    """
    Creates all tables in the database.
    """
    Base.metadata.create_all(bind=engine)
    print("Database migration completed successfully.")


if __name__ == "__main__":
    run_migration()
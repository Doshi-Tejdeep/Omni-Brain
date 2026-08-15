"""
Database migration utility.
"""

from .database import Base, engine


def create_tables():
    """
    Create all database tables and indexes.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()

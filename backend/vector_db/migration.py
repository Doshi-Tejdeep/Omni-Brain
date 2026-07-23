"""
Database Migration Utilities

This file is a placeholder for database migrations.

Future Improvements:
- Integrate Alembic for version-controlled migrations.
- Add schema upgrade and downgrade support.
- Automate migration execution during deployment.
"""

from .database import Base, engine


def create_tables():
    """
    Create all database tables.

    Currently uses SQLAlchemy's create_all().
    This will later be replaced with proper migrations.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


def drop_tables():
    """
    Drop all database tables.

    Useful during development and testing.
    """
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully.")


if __name__ == "__main__":
    create_tables()
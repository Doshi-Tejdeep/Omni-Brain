# Vector Database

This module contains the database configuration, ORM models, schemas, and related files for the Vector Database.

## Database Migration

Current implementation uses SQLAlchemy's `create_all()` to generate tables.

Migration support (Alembic or another migration tool) will be integrated in future iterations to enable version-controlled schema changes.


## History Module

The History table stores previous user interactions.

Fields:
- id
- question
- answer
- created_at

This will later be connected to the Ask API and chat interface.
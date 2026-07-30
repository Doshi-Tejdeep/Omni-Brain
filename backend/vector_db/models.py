"""
Database models (Day 7 - History)
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(
        String,
        nullable=False,
        index=True,
    )

    upload_time = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

    status = Column(
        String,
        default="uploaded",
        index=True,
    )

    page_count = Column(
        Integer,
        default=0,
    )


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )
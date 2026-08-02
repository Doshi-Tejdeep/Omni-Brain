"""
Database schemas and metadata definitions.
"""

from datetime import datetime
from pydantic import BaseModel


# ==========================
# HISTORY SCHEMAS
# ==========================

class HistoryBase(BaseModel):
    session_id: str
    question: str
    answer: str


class HistoryCreate(HistoryBase):
    pass


class HistoryResponse(HistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================
# SESSION SCHEMAS
# ==========================

class SessionBase(BaseModel):
    session_id: str
    title: str


class SessionCreate(SessionBase):
    pass


class SessionResponse(SessionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
"""
Pydantic schemas for the Vector Database module.
"""

from datetime import datetime

from pydantic import BaseModel


# -------------------------
# Document Schemas
# -------------------------

class DocumentBase(BaseModel):
    filename: str
    status: str = "uploaded"
    page_count: int = 0


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    upload_time: datetime

    class Config:
        from_attributes = True


# -------------------------
# History Schemas
# -------------------------

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
"""
Database schemas and metadata definitions.
"""
from datetime import datetime

class HistoryBase(BaseModel):
    question: str
    answer: str


class HistoryCreate(HistoryBase):
    pass


class HistoryResponse(HistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
"""
CRUD operations for the Vector Database module.
"""

from sqlalchemy.orm import Session

from .models import Document, History


# ==========================
# DOCUMENT CRUD
# ==========================


def create_document(db: Session, document: Document):
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()


def get_all_documents(db: Session):
    return db.query(Document).all()


def update_document(db: Session, document_id: int, **kwargs):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        return None

    for key, value in kwargs.items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)

    return document


def delete_document(db: Session, document_id: int):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        return None

    db.delete(document)
    db.commit()

    return document


# ==========================
# HISTORY CRUD
# ==========================


def create_history(db: Session, history: History):
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_history(db: Session):
    return db.query(History).all()


def get_history_by_id(db: Session, history_id: int):
    return db.query(History).filter(History.id == history_id).first()


def delete_history(db: Session, history_id: int):
    history = db.query(History).filter(History.id == history_id).first()

    if not history:
        return None

    db.delete(history)
    db.commit()

    return history

"""
CRUD operations for the Vector Database module.
"""

from sqlalchemy.orm import Session as DBSession

from .models import Document, History


# ==========================
# DOCUMENT CRUD
# ==========================

def create_document(db: DBSession, document: Document):
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document(db: DBSession, document_id: int):
    return (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )


def get_all_documents(db: DBSession):
    return db.query(Document).all()


def update_document(db: DBSession, document_id: int, **kwargs):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        return None

    for key, value in kwargs.items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)

    return document


def delete_document(db: DBSession, document_id: int):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        return None

    db.delete(document)
    db.commit()

    return document


# ==========================
# HISTORY CRUD
# ==========================

def create_history(db: DBSession, history: History):
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_history(db: DBSession):
    return db.query(History).all()


def get_history_by_id(db: DBSession, history_id: int):
    return (
        db.query(History)
        .filter(History.id == history_id)
        .first()
    )


def delete_history(db: DBSession, history_id: int):
    history = (
        db.query(History)
        .filter(History.id == history_id)
        .first()
    )

    if not history:
        return None

    db.delete(history)
    db.commit()

    return history

# ==========================
# SESSION CRUD
# ==========================

from .models import Session


# CREATE SESSION
def create_session(db: Session, session: Session):
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


# GET SESSION BY SESSION_ID
def get_session(db: Session, session_id: str):
    return (
        db.query(Session)
        .filter(Session.session_id == session_id)
        .first()
    )


# GET ALL SESSIONS
def get_all_sessions(db: Session):
    return db.query(Session).all()


# DELETE SESSION
def delete_session(db: Session, session_id: str):
    session = (
        db.query(Session)
        .filter(Session.session_id == session_id)
        .first()
    )

    if not session:
        return None

    db.delete(session)
    db.commit()

    return session
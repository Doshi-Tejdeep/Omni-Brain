"""
CRUD operations for the Vector Database module.
"""

from sqlalchemy.orm import Session as DBSession

from .models import Document, History, Session


# ==========================
# DOCUMENT CRUD
# ==========================


def create_document(db: DBSession, document: Document):
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document(db: DBSession, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()


def get_all_documents(db: DBSession):
    return db.query(Document).all()


def update_document(db: DBSession, document_id: int, **kwargs):
    document = get_document(db, document_id)

    if not document:
        return None

    for key, value in kwargs.items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)
    return document


def delete_document(db: DBSession, document_id: int):
    document = get_document(db, document_id)

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
    return db.query(History).filter(History.id == history_id).first()


def delete_history(db: DBSession, history_id: int):
    history = get_history_by_id(db, history_id)

    if not history:
        return None

    db.delete(history)
    db.commit()
    return history


# ==========================
# SESSION CRUD
# ==========================


def create_session(db: DBSession, session: Session):
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: DBSession, session_id: str):
    return db.query(Session).filter(Session.session_id == session_id).first()


def get_all_sessions(db: DBSession):
    return db.query(Session).all()


def delete_session(db: DBSession, session_id: str):
    session = get_session(db, session_id)

    if not session:
        return None

    db.delete(session)
    db.commit()
    return session


# ==========================
# CHAT HISTORY CRUD
# ==========================


def create_chat_history(db: DBSession, history: History):
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_chat_history(db: DBSession, session_id: str):
    return (
        db.query(History)
        .filter(History.session_id == session_id)
        .order_by(History.created_at.asc())
        .all()
    )


def delete_chat_history(db: DBSession, session_id: str):
    history = db.query(History).filter(History.session_id == session_id).all()

    if not history:
        return None

    for message in history:
        db.delete(message)

    db.commit()
    return True


# ==========================
# CONVERSATION MANAGEMENT
# ==========================


def rename_session(db: DBSession, session_id: str, new_title: str):
    session = db.query(Session).filter(Session.session_id == session_id).first()

    if not session:
        return None

    session.title = new_title

    db.commit()
    db.refresh(session)

    return session


def get_recent_sessions(db: DBSession, limit: int = 10):
    return db.query(Session).order_by(Session.created_at.desc()).limit(limit).all()


def delete_conversation(db: DBSession, session_id: str):
    delete_chat_history(db, session_id)

    session = db.query(Session).filter(Session.session_id == session_id).first()

    if session:
        db.delete(session)
        db.commit()

    return True

from sqlalchemy.orm import Session

from .models import Document


# CREATE
def create_document(db: Session, document: Document):
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


# READ (Single Document)
def get_document(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()


# READ (All Documents)
def get_all_documents(db: Session):
    return db.query(Document).all()


# UPDATE
def update_document(db: Session, document_id: int, **kwargs):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        return None

    for key, value in kwargs.items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)
    return document


# DELETE
def delete_document(db: Session, document_id: int):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        return None

    db.delete(document)
    db.commit()

    return document
"""
SQL service for handling database-related queries.
"""

from backend.vector_db.database import SessionLocal
from backend.vector_db.crud import (
    get_all_documents,
    get_all_sessions,
    get_recent_sessions,
    get_chat_history,
)


"""
SQL service for handling database-related queries.
"""

from backend.vector_db.database import SessionLocal
from backend.vector_db.crud import (
    get_all_documents,
    get_all_sessions,
    get_recent_sessions,
    get_chat_history,
)

DOCUMENT_KEYWORDS = {
    "document",
    "documents",
    "file",
    "files",
    "pdf",
    "pdfs",
}

SESSION_KEYWORDS = {
    "session",
    "sessions",
    "conversation",
    "conversations",
}

HISTORY_KEYWORDS = {
    "history",
    "chat history",
    "messages",
}


def process_sql_query(query: str) -> str:
    """
    Process simple database-related queries.
    """

    db = SessionLocal()

    try:
        query = query.lower()

        if any(keyword in query for keyword in DOCUMENT_KEYWORDS):
            documents = get_all_documents(db)

            if not documents:
                return "No documents found."

            return "\n".join(
                f"- {document.filename}"
                for document in documents
            )

        if (
            "recent" in query
            and any(keyword in query for keyword in SESSION_KEYWORDS)
        ):
            sessions = get_recent_sessions(db)

            if not sessions:
                return "No recent sessions found."

            return "\n".join(
                f"- {session.title}"
                for session in sessions
            )

        if any(keyword in query for keyword in SESSION_KEYWORDS):
            sessions = get_all_sessions(db)

            if not sessions:
                return "No sessions found."

            return "\n".join(
                f"- {session.title}"
                for session in sessions
            )

        if any(keyword in query for keyword in HISTORY_KEYWORDS):
            return (
                "Please specify the session ID to retrieve "
                "chat history."
            )

        return "Unsupported database query."

    finally:
        db.close()
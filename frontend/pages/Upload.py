from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

import streamlit as st


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf"}


@dataclass(frozen=True)
class DocumentDetails:
    name: str
    size_bytes: int
    file_hash: str


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def initialise_session_state() -> None:
    if "staged_document" not in st.session_state:
        st.session_state.staged_document = None


def format_file_size(size_bytes: int) -> str:
    return f"{size_bytes / (1024 * 1024):.2f} MB"


def validate_document(uploaded_file) -> tuple[bool, str]:
    """Perform client-side validation before a document reaches the API."""
    file_name = uploaded_file.name
    extension = file_name.rsplit(".", maxsplit=1)[-1].lower() if "." in file_name else ""

    if extension not in ALLOWED_EXTENSIONS:
        return False, "Only PDF documents are supported."

    if uploaded_file.size == 0:
        return False, "The selected document is empty."

    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        return (
            False,
            f"The document exceeds the {MAX_FILE_SIZE_MB} MB upload limit.",
        )

    # Basic file-signature check. This is not a replacement for server-side
    # validation, which must be implemented when the upload API is added.
    file_bytes = uploaded_file.getvalue()
    if not file_bytes.startswith(b"%PDF-"):
        return False, "This file does not appear to be a valid PDF document."

    return True, ""


def build_document_details(uploaded_file) -> DocumentDetails:
    file_bytes = uploaded_file.getvalue()

    return DocumentDetails(
        name=uploaded_file.name,
        size_bytes=uploaded_file.size,
        file_hash=sha256(file_bytes).hexdigest()[:12],
    )


# -------------------------------------------------------------------
# Page
# -------------------------------------------------------------------

initialise_session_state()

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.35rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            color: #6b7280;
            margin-bottom: 1.6rem;
        }
        .document-card {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
            background: #ffffff;
            margin-top: 1rem;
        }
        .document-name {
            font-size: 1rem;
            font-weight: 650;
            color: #111827;
        }
        .document-meta {
            font-size: 0.9rem;
            color: #6b7280;
            margin-top: 0.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Upload document</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Add a PDF document to OmniBrain for analysis and question answering.</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.subheader("Select a document", divider="gray")
    st.caption(
        f"Supported format: PDF · Maximum size: {MAX_FILE_SIZE_MB} MB"
    )

    uploaded_file = st.file_uploader(
        label="Choose a PDF document",
        type=list(ALLOWED_EXTENSIONS),
        label_visibility="collapsed",
        help="Select one PDF document for processing.",
    )

    if uploaded_file is None:
        st.info("No document selected yet.", icon="ℹ️")

    else:
        is_valid, validation_message = validate_document(uploaded_file)

        if not is_valid:
            st.error(validation_message, icon="🚫")

        else:
            details = build_document_details(uploaded_file)

            st.markdown(
                f"""
                <div class="document-card">
                    <div class="document-name">{details.name}</div>
                    <div class="document-meta">
                        PDF document · {format_file_size(details.size_bytes)}
                        · ID: {details.file_hash}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            with st.form("document_upload_form", border=False):
                confirmed = st.checkbox(
                    "I confirm that I am authorized to upload this document."
                )

                submitted = st.form_submit_button(
                    "Prepare document for upload",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                if not confirmed:
                    st.warning(
                        "Please confirm that you are authorized to upload this document."
                    )
                else:
                    st.session_state.staged_document = details
                    st.success(
                        "Document validated and prepared successfully. "
                        "It will be sent to the OmniBrain upload API when the backend integration is added."
                    )

if st.session_state.staged_document:
    staged = st.session_state.staged_document

    st.write("")
    st.subheader("Prepared document", divider="gray")

    first_column, second_column = st.columns([4, 1])
    with first_column:
        st.write(f"**{staged.name}**")
        st.caption(
            f"PDF document · {format_file_size(staged.size_bytes)} · "
            f"ID: {staged.file_hash}"
        )

    with second_column:
        if st.button("Remove", use_container_width=True):
            st.session_state.staged_document = None
            st.rerun()
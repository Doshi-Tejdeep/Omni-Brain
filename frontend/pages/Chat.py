from __future__ import annotations

import streamlit as st


def initialise_session_state() -> None:
    """Create the chat session only once per browser session."""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Welcome to OmniBrain. Upload a document, then ask me "
                    "questions about its content."
                ),
            }
        ]


def clear_chat() -> None:
    """Reset the conversation to the welcome message."""
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Chat cleared. Upload a document, then ask me a question "
                "about its content."
            ),
        }
    ]


def build_placeholder_response(question: str) -> str:
    """
    Temporary Day 3 response.
    Replace this function with the Ask API call when the backend endpoint
    is available later in the project.
    """
    return (
        "Your question has been added to the conversation. "
        "OmniBrain's answer-generation service will be connected in a later "
        "integration phase."
    )


initialise_session_state()

st.markdown(
    """
    <style>
        .chat-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.2rem;
        }

        .chat-subtitle {
            color: #6b7280;
            font-size: 1rem;
            margin-bottom: 1.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown('<div class="chat-title">OmniBrain Chat</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="chat-subtitle">'
        'Ask questions about your uploaded documents.'
        '</div>',
        unsafe_allow_html=True,
    )

with header_right:
    st.write("")
    if st.button("Clear chat", use_container_width=True):
        clear_chat()
        st.rerun()

st.divider()

uploaded_document = st.session_state.get("staged_document")

if uploaded_document:
    document_name = uploaded_document.name
    st.success(f"Document ready: {document_name}", icon="✓")
else:
    st.info(
        "No document has been prepared yet. You can still use the chat interface, "
        "but upload a document for document-based answers.",
        icon="ℹ️",
    )

# Display existing conversation history.
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Add a new user message and a temporary assistant reply.
question = st.chat_input("Ask a question about your document...")

if question:
    user_message = {"role": "user", "content": question}
    st.session_state.chat_messages.append(user_message)

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("OmniBrain is preparing a response..."):
            response = build_placeholder_response(question)
            st.write(response)

    st.session_state.chat_messages.append(
        {"role": "assistant", "content": response}
    )
"""
pages/Chat.py — OmniBrain Ask page
"""

import streamlit as st
import requests

st.set_page_config(
    page_title="OmniBrain — Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
defaults = {
    "uploaded_file": None,
    "chat_history": [],
    "questions_asked": 0,
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

# ---------------------------------------------------------
# THEME
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #f0f0f0;
    }
    .stTextInput > div > div > input {
        background-color: #1e1b3a;
        color: #ffffff;
        border: 1px solid #7b2ff7;
        border-radius: 8px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #7b2ff7, #f107a3);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 12px rgba(241, 7, 163, 0.6);
    }
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧠 OmniBrain")
    st.caption("AI Document Intelligence")
    st.markdown("---")

    if st.session_state.uploaded_file:
        st.success(f"Loaded: {st.session_state.uploaded_file}")
    else:
        st.info("No document loaded. Go to Upload first.")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("💬 Ask OmniBrain")

if st.session_state.uploaded_file:
    st.caption(f"Chatting with: **{st.session_state.uploaded_file}**")
else:
    st.caption("No document loaded yet — answers won't be grounded in your file.")

st.markdown("---")

# ---------------------------------------------------------
# ASK / ANSWER SECTION
# ---------------------------------------------------------
st.subheader("Ask OmniBrain")

col1, col2 = st.columns([5, 1])
with col1:
    user_question = st.text_input(
        "Your question",
        placeholder="e.g. Summarize the key findings in this document",
        label_visibility="collapsed",
    )
with col2:
    ask_clicked = st.button("Ask", use_container_width=True)

if ask_clicked:
    if not user_question.strip():
        st.warning("Please type a question before asking.")
    else:
        with st.spinner("Thinking... this can take a minute on first run."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"question": user_question},
                    timeout=180,
                )
                response.raise_for_status()
                data = response.json()
                answer = data.get("answer", "No answer returned.")

                st.session_state.chat_history.append(
                    {"question": user_question, "answer": answer}
                )
                st.session_state.questions_asked += 1

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the backend at "
                    f"{BACKEND_URL}. Make sure uvicorn is running."
                )
            except requests.exceptions.Timeout:
                st.error(
                    "The backend took too long to respond (over 3 minutes). "
                    "The AI model may be running slowly. Try again."
                )
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

# ---------------------------------------------------------
# DISPLAY CONVERSATION
# ---------------------------------------------------------
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("Conversation")
    st.caption(f"{st.session_state.questions_asked} question(s) asked this session")

    for entry in reversed(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(entry["question"])
        with st.chat_message("assistant"):
            st.write(entry["answer"])

    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.session_state.questions_asked = 0
        st.rerun()
else:
    st.markdown("---")
    st.caption("Your conversation will appear here once you ask a question.")
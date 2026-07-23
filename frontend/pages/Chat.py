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

# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────────────────
defaults = {
    "uploaded_file": None,
    "chat_history": [],
    "questions_asked": 0,
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

# ──────────────────────────────────────────────────────────────────────────
# THEME (same palette as app.py — keep in sync if you change one)
# ──────────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-deep:      #0b0f19;
    --bg-panel:     #121729;
    --bg-card:      #161c30;
    --accent-1:     #7c3aed;
    --accent-2:     #ec4899;
    --accent-3:     #06b6d4;
    --text-main:    #eef1f8;
    --text-muted:   #9aa3b8;
    --border-soft:  rgba(255,255,255,0.08);
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    background: transparent !important;
    box-shadow: none !important;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0b0f19, #121729, #1a1035, #0b0f19) !important;
    background-size: 400% 400% !important;
    animation: gradientShift 18s ease infinite;
    color: var(--text-main);
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.block-container { animation: fadeInUp 0.6s ease-out; }

section[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border-soft);
}
section[data-testid="stSidebar"] * { color: var(--text-main); }

h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    font-weight: 800 !important;
}

.answer-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-left: 3px solid var(--accent-3);
    border-radius: 12px;
    padding: 16px 18px;
    line-height: 1.55;
    animation: fadeInUp 0.4s ease-out;
}

div.stButton > button {
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6em 1.4em;
    font-weight: 600;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(124,58,237,0.4);
}

hr { border-color: var(--border-soft) !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧠 OmniBrain")
    st.caption("AI Document Intelligence")
    st.markdown("---")
    if st.session_state.uploaded_file is None:
        st.info("Upload a document to begin", icon="ℹ️")
    else:
        st.success(f"Loaded: {st.session_state.uploaded_file}", icon="✅")

# ──────────────────────────────────────────────────────────────────────────
# MAIN — CHAT
# ──────────────────────────────────────────────────────────────────────────
st.markdown("## 💬 Ask OmniBrain")

if st.session_state.uploaded_file is None:
    st.warning("Upload a document first to unlock chat.")
    st.page_link("pages/Upload.py", label="Go to Upload Center →")
else:
    st.caption(f"Chatting with: **{st.session_state.uploaded_file}**")

    # replay previous turns
    for turn in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(turn["question"])
        with st.chat_message("assistant"):
            st.markdown(f'<div class="answer-card">{turn["answer"]}</div>', unsafe_allow_html=True)
            if turn.get("sources"):
                with st.expander(f"📚 Sources ({len(turn['sources'])})"):
                    for src in turn["sources"]:
                        st.markdown(f"- {src}")

    query = st.chat_input("Ask a question about your document...")
    if query:
        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(
                        f"{BACKEND_URL}/ask",
                        json={"question": query},
                        timeout=30,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        answer = data.get("answer", "No answer returned.")
                        sources = data.get("sources", [])
                    else:
                        answer = f"⚠️ Backend returned an error ({resp.status_code}). Please try again."
                        sources = []
                except requests.exceptions.ConnectionError:
                    answer = "⚠️ Can't reach the backend. Start FastAPI at http://127.0.0.1:8000."
                    sources = []
                except requests.exceptions.Timeout:
                    answer = "⚠️ The request timed out. Please try again."
                    sources = []

            st.markdown(f'<div class="answer-card">{answer}</div>', unsafe_allow_html=True)
            if sources:
                with st.expander(f"📚 Sources ({len(sources)})"):
                    for src in sources:
                        st.markdown(f"- {src}")

        st.session_state.questions_asked += 1
        st.session_state.chat_history.append(
            {"question": query, "answer": answer, "sources": sources}
        )
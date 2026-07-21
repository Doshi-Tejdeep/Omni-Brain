"""
OmniBrain — Chat Page (v2)
Matches the exact theme/animation system used in app.py.

Use as a Streamlit multipage file:  pages/1_💬_Chat.py
(or run standalone:  streamlit run chat.py)
"""

import streamlit as st
import time
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OmniBrain — Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "questions_asked": 0,
    "uploaded_file": None,
    "prepared_docs": 0,
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

# ──────────────────────────────────────────────────────────────────────────
# THEME + ANIMATION (identical system to app.py, plus chat-specific bits)
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

/* ---- kill the white Streamlit chrome: header / toolbar / decoration bar ---- */
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    background: transparent !important;
    box-shadow: none !important;
}

/* Theme the whole viewport so no white strip shows on scroll/resize */
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

/* ---- floating particles behind everything ---- */
.particle-field { position: fixed; inset: 0; overflow: hidden; z-index: 0; pointer-events: none; }
.particle {
    position: absolute;
    bottom: -10%;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(124,58,237,0.55), transparent 70%);
    animation: floatUp linear infinite;
}
@keyframes floatUp {
    0%   { transform: translateY(0) translateX(0); opacity: 0; }
    10%  { opacity: 0.7; }
    100% { transform: translateY(-115vh) translateX(40px); opacity: 0; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.block-container { animation: fadeInUp 0.5s ease-out; position: relative; z-index: 1; }

section[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border-soft);
}
section[data-testid="stSidebar"] * { color: var(--text-main); }

h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

/* ---- chat header ---- */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, rgba(124,58,237,0.15), rgba(6,182,212,0.10));
    border: 1px solid var(--border-soft);
    border-left: 4px solid var(--accent-3);
    padding: 16px 22px;
    border-radius: 12px;
    margin-bottom: 20px;
    animation: fadeInUp 0.5s ease-out;
}
.chat-header .doc-name { font-weight: 600; }
.chat-header .doc-sub  { color: var(--text-muted); font-size: 13px; }

/* ---- chat bubbles ---- */
@keyframes bubbleIn {
    from { opacity: 0; transform: translateY(10px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
div[data-testid="stChatMessage"] {
    animation: bubbleIn 0.35s ease-out;
    border-radius: 14px;
    margin-bottom: 4px;
    background: var(--bg-card) !important;
    border: 1px solid var(--border-soft);
}

/* typing indicator dots */
.typing-dots span {
    display: inline-block;
    width: 6px; height: 6px;
    margin-right: 4px;
    border-radius: 50%;
    background: var(--accent-3);
    animation: typingBounce 1.2s infinite ease-in-out;
}
.typing-dots span:nth-child(2) { animation-delay: 0.15s; }
.typing-dots span:nth-child(3) { animation-delay: 0.3s; }
@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
    30%           { transform: translateY(-5px); opacity: 1; }
}

/* ---- suggestion chips / buttons ---- */
div.stButton > button {
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55em 1.2em;
    font-weight: 600;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(124,58,237,0.4);
}
div.stButton > button:active { transform: translateY(0) scale(0.98); }

/* ---- status pills (shared with app.py) ---- */
.status-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.pill { padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
.pill.online   { background: rgba(16,185,129,0.15); color: #10b981; }
.pill.ready    { background: rgba(6,182,212,0.15); color: #06b6d4; }
.pill.pending  { background: rgba(234,179,8,0.15); color: #eab308; }

/* ---- progress ring (shared with app.py) ---- */
.ring-wrap { display: flex; align-items: center; gap: 14px; }
.ring {
    width: 46px; height: 46px;
    border-radius: 50%;
    background: conic-gradient(var(--accent-3) calc(var(--pct) * 1%), rgba(255,255,255,0.08) 0);
    display: flex; align-items: center; justify-content: center;
}
.ring::after { content: ""; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-card); }

/* ---- empty state ---- */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    border: 1px dashed var(--border-soft);
    border-radius: 16px;
    color: var(--text-muted);
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    z-index: 1;
}

/* ---- scrollbar ---- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--accent-1); border-radius: 8px; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# floating particle field — identical positions/timings to app.py for visual continuity
particles_html = '<div class="particle-field">'
sizes  = [18, 26, 14, 32, 20, 24, 16, 28]
lefts  = [5, 15, 27, 40, 55, 68, 80, 92]
durs   = [14, 18, 22, 16, 20, 24, 15, 19]
delays = [0, 3, 6, 2, 9, 1, 5, 8]
for s, l, d, dl in zip(sizes, lefts, durs, delays):
    particles_html += (
        f'<div class="particle" style="width:{s}px;height:{s}px;'
        f'left:{l}%;animation-duration:{d}s;animation-delay:{dl}s;"></div>'
    )
particles_html += "</div>"
st.markdown(particles_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧠 OmniBrain")
    st.caption("AI Document Intelligence")
    st.markdown("---")

    if hasattr(st, "page_link"):
        try:
            st.page_link("app.py", label="🏠 Home")
        except Exception:
            pass

    st.markdown("---")

    if st.session_state.uploaded_file:
        st.success(f"Active document: {st.session_state.uploaded_file}", icon="📄")
    else:
        st.warning("No document loaded", icon="⚠️")

    st.markdown("---")
    st.markdown("**SESSION**")
    st.markdown(
        f"""
        <div class="status-row"><span>Questions asked</span><span class="pill ready">{st.session_state.questions_asked}</span></div>
        <div class="status-row"><span>Documents prepared</span><span class="pill online">{st.session_state.prepared_docs}</span></div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    readiness_pct = 100 if st.session_state.uploaded_file else 15
    st.markdown(
        f"""
        <div class="ring-wrap">
            <div class="ring" style="--pct:{readiness_pct};"></div>
            <div>
                <div style="font-weight:600;">Session readiness</div>
                <div style="color:var(--text-muted); font-size:12px;">{readiness_pct}% configured</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────
doc_name = st.session_state.uploaded_file or "No document loaded"
doc_sub = (
    "Ask focused questions and get grounded, cited answers."
    if st.session_state.uploaded_file
    else "Upload a document from the Home page to unlock chat."
)

st.markdown(
    f"""
    <div class="chat-header">
        <div>
            <div class="doc-name">💬 Ask OmniBrain</div>
            <div class="doc-sub">{doc_sub}</div>
        </div>
        <div class="doc-name">📄 {doc_name}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# GUARD: no document uploaded yet
# ──────────────────────────────────────────────────────────────────────────
if not st.session_state.uploaded_file:
    st.markdown(
        """
        <div class="empty-state">
            <h3>📄 No document to chat with yet</h3>
            <p>Head back to the Home page and upload a PDF to unlock this chat.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ──────────────────────────────────────────────────────────────────────────
# SUGGESTION CHIPS (only before first message)
# ──────────────────────────────────────────────────────────────────────────
clicked = None
if not st.session_state.messages:
    st.markdown("##### Try asking:")
    c1, c2, c3 = st.columns(3)
    suggestions = [
        "Summarize this document",
        "What are the key points?",
        "List any dates or figures mentioned",
    ]
    for col, text in zip([c1, c2, c3], suggestions):
        with col:
            if st.button(text, key=f"chip_{text}", use_container_width=True):
                clicked = text

# ──────────────────────────────────────────────────────────────────────────
# CHAT HISTORY
# ──────────────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "time" in msg:
            st.caption(msg["time"])

# ──────────────────────────────────────────────────────────────────────────
# CHAT INPUT
# ──────────────────────────────────────────────────────────────────────────
user_query = st.chat_input("Ask a question about your document...")
query = clicked or user_query


def generate_answer(question: str) -> str:
    """
    Placeholder response generator.
    Replace this with a call to your real retrieval/AI backend, e.g.:

        response = your_rag_pipeline.query(question, document=st.session_state.uploaded_file)
        return response
    """
    return (
        "🔌 This is a placeholder answer. Connect this function to your "
        "document retrieval + AI backend to generate real, grounded responses."
    )


if query:
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": query, "time": timestamp})
    st.session_state.questions_asked += 1

    with st.chat_message("user"):
        st.write(query)
        st.caption(timestamp)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown(
            '<span class="typing-dots"><span></span><span></span><span></span></span>',
            unsafe_allow_html=True,
        )
        time.sleep(1.1)
        answer = generate_answer(query)
        placeholder.write(answer)
        reply_time = datetime.now().strftime("%H:%M")
        st.caption(reply_time)

    st.session_state.messages.append({"role": "assistant", "content": answer, "time": reply_time})
    st.rerun()
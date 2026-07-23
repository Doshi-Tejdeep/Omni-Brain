"""
OmniBrain — AI Document Intelligence
Polished, fully-themed, animated Streamlit front-end (v2).

Run with:  streamlit run app.py
"""

import streamlit as st
import time

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OmniBrain — AI Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────────────────
defaults = {
    "prepared_docs": 0,
    "questions_asked": 0,
    "workspace_status": "Waiting for upload",
    "uploaded_file": None,
    "page": "Home",
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

# ──────────────────────────────────────────────────────────────────────────
# THEME + ANIMATION (CSS)
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

/* Theme the whole viewport, not just block-container, so no white strip
   shows behind the header on scroll/resize. */
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
.particle-field {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: 0;
    pointer-events: none;
}
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

/* ---- fade + rise entrance ---- */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.block-container { animation: fadeInUp 0.6s ease-out; position: relative; z-index: 1; }

/* ---- sidebar ---- */
section[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border-soft);
}
section[data-testid="stSidebar"] * { color: var(--text-main); }

/* ---- headings ---- */
h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

/* ---- hero / typing headline ---- */
.hero {
    text-align: center;
    padding: 10px 0 26px 0;
    animation: fadeInUp 0.6s ease-out;
}
.hero .eyebrow {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.hero h1 { font-size: 42px; margin: 6px 0 4px 0; }
.hero .typed {
    border-right: 2px solid var(--accent-3);
    white-space: nowrap;
    overflow: hidden;
    display: inline-block;
    animation: typing 3.2s steps(38, end) infinite alternate, blink 0.75s step-end infinite;
}
@keyframes typing { from { width: 0; } to { width: 30ch; } }
@keyframes blink { 50% { border-color: transparent; } }

.gradient-text {
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2) 60%, var(--accent-3));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

/* ---- banner ---- */
.banner {
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(90deg, rgba(124,58,237,0.15), rgba(236,72,153,0.10));
    border: 1px solid var(--border-soft);
    border-left: 4px solid var(--accent-1);
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 28px;
    animation: fadeInUp 0.5s ease-out;
}
.banner .dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: var(--accent-3);
    animation: pulse 1.8s infinite;
    flex-shrink: 0;
}
@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(6,182,212,0.55); }
    70%  { box-shadow: 0 0 0 10px rgba(6,182,212,0); }
    100% { box-shadow: 0 0 0 0 rgba(6,182,212,0); }
}

/* ---- feature cards ---- */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 16px;
    padding: 28px;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
    animation: fadeInUp 0.7s ease-out;
}
.card::before {
    content: "";
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(124,58,237,0.08), transparent 30%);
    animation: rotateGlow 6s linear infinite;
    opacity: 0;
    transition: opacity 0.3s ease;
}
.card:hover::before { opacity: 1; }
@keyframes rotateGlow { to { transform: rotate(360deg); } }
.card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 18px 40px rgba(124,58,237,0.25);
    border-color: var(--accent-1);
}
.card h3 { margin-top: 0; position: relative; z-index: 1; }
.card p { color: var(--text-muted); position: relative; z-index: 1; }

/* ---- step cards ---- */
.step-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 22px;
    text-align: left;
    transition: transform 0.25s ease, border-color 0.25s ease;
}
.step-card:hover { transform: translateY(-4px); border-color: var(--accent-3); }
.step-num {
    display: inline-block;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-3));
    color: white;
    font-weight: 700;
    font-size: 13px;
    padding: 4px 10px;
    border-radius: 999px;
    margin-bottom: 10px;
}

/* ---- metrics ---- */
.metric-box {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 20px 24px;
    transition: transform 0.25s ease;
    animation: fadeInUp 0.8s ease-out;
}
.metric-box:hover { transform: translateY(-3px); }
.metric-label {
    color: var(--text-muted);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 36px;
    font-weight: 800;
    margin-top: 4px;
}
.metric-value.shimmer {
    background: linear-gradient(90deg, var(--text-main) 25%, var(--accent-3) 50%, var(--text-main) 75%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
    0%   { background-position: 200% center; }
    100% { background-position: -200% center; }
}

/* ---- progress ring for workspace readiness ---- */
.ring-wrap { display: flex; align-items: center; gap: 14px; }
.ring {
    width: 46px; height: 46px;
    border-radius: 50%;
    background: conic-gradient(var(--accent-3) calc(var(--pct) * 1%), rgba(255,255,255,0.08) 0);
    display: flex; align-items: center; justify-content: center;
    transition: background 0.6s ease;
}
.ring::after {
    content: "";
    width: 32px; height: 32px;
    border-radius: 50%;
    background: var(--bg-card);
}

/* ---- status pills ---- */
.status-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.pill { padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
.pill.online   { background: rgba(16,185,129,0.15); color: #10b981; }
.pill.ready    { background: rgba(6,182,212,0.15); color: #06b6d4; }
.pill.pending  { background: rgba(234,179,8,0.15); color: #eab308; }

/* ---- buttons ---- */
div.stButton > button {
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6em 1.4em;
    font-weight: 600;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(124,58,237,0.4);
}
div.stButton > button:active { transform: translateY(0) scale(0.98); }

/* ---- radio nav styled as pill tabs ---- */
div[role="radiogroup"] label {
    border-radius: 10px;
    padding: 6px 10px;
    transition: background 0.2s ease;
}
div[role="radiogroup"] label:hover { background: rgba(255,255,255,0.06); }

/* ---- file uploader drag state polish ---- */
[data-testid="stFileUploaderDropzone"] {
    border: 1.5px dashed var(--border-soft) !important;
    background: rgba(255,255,255,0.02) !important;
    transition: border-color 0.25s ease, background 0.25s ease;
    border-radius: 14px !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--accent-3) !important;
    background: rgba(6,182,212,0.05) !important;
}

/* ---- divider ---- */
hr { border-color: var(--border-soft) !important; }

/* ---- scrollbar ---- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--accent-1); border-radius: 8px; }

/* ---- hide default streamlit chrome ---- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# floating particle field (purely decorative, positions/timings varied inline)
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

    nav_options = ["Home", "Chat", "Upload"]
    current_idx = nav_options.index(st.session_state.page) if st.session_state.page in nav_options else 0
    st.session_state.page = st.radio(
        "Navigate", nav_options, index=current_idx, label_visibility="collapsed"
    )

    st.markdown("---")

    if st.session_state.uploaded_file is None:
        st.info("Upload a document to begin", icon="ℹ️")
    else:
        st.success(f"Loaded: {st.session_state.uploaded_file}", icon="✅")

    st.markdown("---")
    st.markdown("**SYSTEM STATUS**")
    st.markdown(
        """
        <div class="status-row"><span>Frontend</span><span class="pill online">Online</span></div>
        <div class="status-row"><span>Document service</span><span class="pill ready">Ready</span></div>
        <div class="status-row"><span>AI answers</span><span class="pill pending">Integration pending</span></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    readiness_pct = 100 if st.session_state.uploaded_file else 15
    st.markdown(
        f"""
        <div class="ring-wrap">
            <div class="ring" style="--pct:{readiness_pct};"></div>
            <div>
                <div style="font-weight:600;">Workspace readiness</div>
                <div style="color:var(--text-muted); font-size:12px;">{readiness_pct}% configured</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────────────────
# HOME PAGE
# ──────────────────────────────────────────────────────────────────────────
if st.session_state.page == "Home":
    st.markdown(
        """
        <div class="hero">
            <span class="eyebrow">AI Document Intelligence</span>
            <h1><span class="gradient-text">OmniBrain</span></h1>
            <div class="typed">Upload. Prepare. Ask anything.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="banner">
            <div class="dot"></div>
            <div>Start by uploading a PDF document to unlock document-based chat.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>📤 Upload a document</h3>
                <p>Add a PDF and validate it before preparing it for OmniBrain processing.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Upload Center", key="upload_btn", use_container_width=True):
            st.session_state.page = "Upload"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>💬 Ask OmniBrain</h3>
                <p>Explore your uploaded knowledge with a focused document conversation interface.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open AI Chat", key="chat_btn", use_container_width=True):
            st.session_state.page = "Chat"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("## Workspace overview")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Prepared documents</div>
                <div class="metric-value shimmer">{st.session_state.prepared_docs}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Questions asked</div>
                <div class="metric-value shimmer">{st.session_state.questions_asked}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Workspace status</div>
                <div class="metric-value" style="font-size:26px;">{st.session_state.workspace_status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("## How it works")
    s1, s2, s3 = st.columns(3)
    steps = [
        ("01", "Upload", "Drop in a PDF and let OmniBrain validate its structure and content."),
        ("02", "Prepare", "The document is chunked, indexed, and readied for AI-powered retrieval."),
        ("03", "Ask", "Chat naturally with your document and get grounded, cited answers."),
    ]
    for col, (num, title, desc) in zip([s1, s2, s3], steps):
        with col:
            st.markdown(
                f"""
                <div class="step-card">
                    <span class="step-num">{num}</span>
                    <h4>{title}</h4>
                    <p style="color: var(--text-muted); font-size: 14px;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ──────────────────────────────────────────────────────────────────────────
# UPLOAD PAGE
# ──────────────────────────────────────────────────────────────────────────
elif st.session_state.page == "Upload":
    st.markdown("## 📤 Upload Center")
    st.caption("Add a PDF and validate it before preparing it for OmniBrain processing.")

    file = st.file_uploader("Drag & drop a PDF, or click to browse", type=["pdf"])

    if file is not None:
        progress = st.progress(0, text="Validating document...")
        for pct, label in [(30, "Validating document..."), (65, "Indexing content..."), (100, "Finalizing...")]:
            time.sleep(0.4)
            progress.progress(pct, text=label)

        st.session_state.uploaded_file = file.name
        st.session_state.prepared_docs += 1
        st.session_state.workspace_status = "Ready"
        st.success(f"✅ '{file.name}' is prepared and ready for chat.")
        st.balloons()

        if st.button("Go to Ask OmniBrain →"):
            st.session_state.page = "Chat"
            st.rerun()

# ──────────────────────────────────────────────────────────────────────────
# CHAT PAGE
# ──────────────────────────────────────────────────────────────────────────
elif st.session_state.page == "Chat":
    st.markdown("## 💬 Ask OmniBrain")

    if st.session_state.uploaded_file is None:
        st.warning("Upload a document first to unlock chat.")
        if st.button("Go to Upload Center →"):
            st.session_state.page = "Upload"
            st.rerun()
    else:
        st.caption(f"Chatting with: **{st.session_state.uploaded_file}**")
        query = st.chat_input("Ask a question about your document...")
        if query:
            st.session_state.questions_asked += 1
            with st.chat_message("user"):
                st.write(query)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    time.sleep(1)
                st.write("🔌 Connect this to your AI backend to generate real answers here.")



"""
OmniBrain — Upload Page (v2)
Matches the exact theme/animation system used in app.py and chat.py.

Use as a Streamlit multipage file:  pages/2_📤_Upload.py
(or run standalone:  streamlit run upload.py)
"""

import streamlit as st
import time

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OmniBrain — Upload",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────────────────
defaults = {
    "uploaded_file": None,
    "prepared_docs": 0,
    "workspace_status": "Waiting for upload",
    "questions_asked": 0,
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

MAX_FILE_MB = 50

# ──────────────────────────────────────────────────────────────────────────
# THEME + ANIMATION (identical system to app.py / chat.py)
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
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.block-container { animation: fadeInUp 0.6s ease-out; position: relative; z-index: 1; }

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

/* ---- eyebrow badge ---- */
.eyebrow {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 18px;
    animation: fadeInUp 0.5s ease-out;
}

.page-title {
    font-size: 44px;
    margin: 4px 0 10px 0;
    animation: fadeInUp 0.6s ease-out;
}
.page-sub {
    color: var(--text-muted);
    font-size: 17px;
    margin-bottom: 28px;
    animation: fadeInUp 0.7s ease-out;
}

/* ---- upload card ---- */
.upload-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 18px;
    padding: 30px;
    animation: fadeInUp 0.75s ease-out;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.upload-card:hover {
    border-color: rgba(124,58,237,0.35);
    box-shadow: 0 18px 40px rgba(124,58,237,0.12);
}
.upload-card h4 { margin-top: 0; }

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

/* ---- info banner ---- */
.banner {
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(90deg, rgba(6,182,212,0.14), rgba(124,58,237,0.08));
    border: 1px solid var(--border-soft);
    border-left: 4px solid var(--accent-3);
    padding: 16px 20px;
    border-radius: 12px;
    margin: 22px 0;
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
.banner.success { border-left-color: #10b981; background: linear-gradient(90deg, rgba(16,185,129,0.14), rgba(6,182,212,0.06)); }
.banner.success .dot { background: #10b981; }

/* ---- security note ---- */
.security-note {
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.6;
    border-top: 1px solid var(--border-soft);
    padding-top: 18px;
    margin-top: 30px;
    animation: fadeInUp 0.9s ease-out;
}

/* ---- status pills / ring (shared) ---- */
.status-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.pill { padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
.pill.online   { background: rgba(16,185,129,0.15); color: #10b981; }
.pill.ready    { background: rgba(6,182,212,0.15); color: #06b6d4; }
.pill.pending  { background: rgba(234,179,8,0.15); color: #eab308; }

.ring-wrap { display: flex; align-items: center; gap: 14px; }
.ring {
    width: 46px; height: 46px;
    border-radius: 50%;
    background: conic-gradient(var(--accent-3) calc(var(--pct) * 1%), rgba(255,255,255,0.08) 0);
    display: flex; align-items: center; justify-content: center;
}
.ring::after { content: ""; width: 32px; height: 32px; border-radius: 50%; background: var(--bg-card); }

/* ---- buttons ---- */
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
div.stButton > button:active { transform: translateY(0) scale(0.98); }

hr { border-color: var(--border-soft) !important; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--accent-1); border-radius: 8px; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# floating particle field — same positions/timings as app.py & chat.py
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
# HEADER
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<span class="eyebrow">OmniBrain Document Center</span>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Upload your knowledge</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-sub">Add a PDF securely and prepare it for intelligent document analysis.</div>',
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# UPLOAD CARD
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown("#### Select a PDF document")

file = st.file_uploader(
    " ",
    type=["pdf"],
    label_visibility="collapsed",
    help=f"200MB per file • PDF · enforced limit: {MAX_FILE_MB}MB",
)
st.caption("200MB per file • PDF")
st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# VALIDATION + STATUS BANNER
# ──────────────────────────────────────────────────────────────────────────
if file is None:
    st.markdown(
        f"""
        <div class="banner">
            <div class="dot"></div>
            <div>Select a PDF to begin. Maximum file size: {MAX_FILE_MB} MB.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    size_mb = file.size / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        st.markdown(
            f"""
            <div class="banner" style="border-left-color:#ef4444; background: linear-gradient(90deg, rgba(239,68,68,0.14), rgba(124,58,237,0.06));">
                <div class="dot" style="background:#ef4444;"></div>
                <div>'{file.name}' is {size_mb:.1f} MB — exceeds the {MAX_FILE_MB} MB limit. Please choose a smaller file.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        progress = st.progress(0, text="Validating document...")
        for pct, label in [(35, "Validating document..."), (70, "Indexing content..."), (100, "Finalizing...")]:
            time.sleep(0.35)
            progress.progress(pct, text=label)

        st.session_state.uploaded_file = file.name
        st.session_state.prepared_docs += 1
        st.session_state.workspace_status = "Ready"

        st.markdown(
            f"""
            <div class="banner success">
                <div class="dot"></div>
                <div>'{file.name}' ({size_mb:.1f} MB) is validated and ready for OmniBrain processing.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.balloons()

        if st.button("Go to Ask OmniBrain →"):
            st.switch_page("chat.py") if hasattr(st, "switch_page") else None

# ──────────────────────────────────────────────────────────────────────────
# SECURITY NOTE
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="security-note">
        Security note: This Day 2 interface performs client-side validation.
        Server-side validation and document processing will be added with the backend API.
    </div>
    """,
    unsafe_allow_html=True,
)
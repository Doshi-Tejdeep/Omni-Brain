from hashlib import sha256
from html import escape

import requests
import streamlit as st


# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------

st.set_page_config(
    page_title="OmniBrain - Upload",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

API_BASE_URL = "http://127.0.0.1:8000"
UPLOAD_URL = f"{API_BASE_URL}/upload"

MAX_FILE_MB = 50
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024


# -------------------------------------------------------------------
# Session state
# -------------------------------------------------------------------

defaults = {
    "uploaded_file": None,
    "prepared_docs": 0,
    "workspace_status": "Waiting for upload",
    "questions_asked": 0,
    "processed_document_id": None,
    "last_uploaded_file_id": None,
}

for key, value in defaults.items():
    st.session_state.setdefault(key, value)


# -------------------------------------------------------------------
# Backend and validation helpers
# -------------------------------------------------------------------

@st.cache_data(ttl=10, show_spinner=False)
def is_backend_online() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False


def validate_pdf(uploaded_file) -> tuple[bool, str]:
    if uploaded_file.size == 0:
        return False, "The selected PDF is empty."

    if uploaded_file.size > MAX_FILE_BYTES:
        return False, f"Maximum file size is {MAX_FILE_MB} MB."

    if not uploaded_file.getvalue().startswith(b"%PDF-"):
        return False, "The selected file is not a valid PDF document."

    return True, ""


# -------------------------------------------------------------------
# Theme and animation
# -------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-deep: #0b0f19;
    --bg-panel: #121729;
    --bg-card: #161c30;
    --accent-1: #7c3aed;
    --accent-2: #ec4899;
    --accent-3: #06b6d4;
    --text-main: #eef1f8;
    --text-muted: #9aa3b8;
    --border-soft: rgba(255,255,255,0.08);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

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
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

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
    0% { transform: translateY(0) translateX(0); opacity: 0; }
    10% { opacity: 0.7; }
    100% { transform: translateY(-115vh) translateX(40px); opacity: 0; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

.block-container {
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    z-index: 1;
}

section[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border-soft);
}

section[data-testid="stSidebar"] * {
    color: var(--text-main);
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

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
}

.page-title {
    font-family: 'Sora', sans-serif;
    font-size: 44px;
    font-weight: 800;
    color: var(--text-main);
    margin: 4px 0 10px 0;
}

.page-sub {
    color: var(--text-muted);
    font-size: 17px;
    margin-bottom: 28px;
}

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
    color: var(--text-main);
    animation: fadeInUp 0.5s ease-out;
}

.banner.success {
    border-left-color: #10b981;
    background: linear-gradient(90deg, rgba(16,185,129,0.14), rgba(6,182,212,0.06));
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent-3);
    animation: pulse 1.8s infinite;
    flex-shrink: 0;
}

.banner.success .dot {
    background: #10b981;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(6,182,212,0.55); }
    70% { box-shadow: 0 0 0 10px rgba(6,182,212,0); }
    100% { box-shadow: 0 0 0 0 rgba(6,182,212,0); }
}

.status-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.pill {
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
}

.pill.online {
    background: rgba(16,185,129,0.15);
    color: #10b981;
}

.pill.ready {
    background: rgba(6,182,212,0.15);
    color: #06b6d4;
}

.pill.pending {
    background: rgba(234,179,8,0.15);
    color: #eab308;
}

.ring-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
}

.ring {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: conic-gradient(
        var(--accent-3) calc(var(--pct) * 1%),
        rgba(255,255,255,0.08) 0
    );
    display: flex;
    align-items: center;
    justify-content: center;
}

.ring::after {
    content: "";
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--bg-card);
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

div.stButton > button:active {
    transform: translateY(0) scale(0.98);
}

.security-note {
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.6;
    border-top: 1px solid var(--border-soft);
    padding-top: 18px;
    margin-top: 30px;
}

hr {
    border-color: var(--border-soft) !important;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-deep);
}

::-webkit-scrollbar-thumb {
    background: var(--accent-1);
    border-radius: 8px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -------------------------------------------------------------------
# Animated background particles
# -------------------------------------------------------------------

particles_html = '<div class="particle-field">'

sizes = [18, 26, 14, 32, 20, 24, 16, 28]
lefts = [5, 15, 27, 40, 55, 68, 80, 92]
durations = [14, 18, 22, 16, 20, 24, 15, 19]
delays = [0, 3, 6, 2, 9, 1, 5, 8]

for size, left, duration, delay in zip(sizes, lefts, durations, delays):
    particles_html += (
        f'<div class="particle" style="width:{size}px; height:{size}px; '
        f'left:{left}%; animation-duration:{duration}s; '
        f'animation-delay:{delay}s;"></div>'
    )

particles_html += "</div>"

st.markdown(particles_html, unsafe_allow_html=True)


# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------

backend_online = is_backend_online()

with st.sidebar:
    st.markdown("### 🧠 OmniBrain")
    st.caption("AI Document Intelligence")
    st.markdown("---")

    try:
        st.page_link("app.py", label="Home", icon="🏠")
    except Exception:
        pass

    st.markdown("---")

    if st.session_state.uploaded_file is None:
        st.info("Upload a document to begin", icon="ℹ️")
    else:
        st.success(
            f"Loaded: {st.session_state.uploaded_file}",
            icon="✅",
        )

    st.markdown("---")
    st.markdown("**SYSTEM STATUS**")

    backend_label = "Online" if backend_online else "Offline"
    backend_class = "online" if backend_online else "pending"

    st.markdown(
        f"""
        <div class="status-row">
            <span>Frontend</span>
            <span class="pill online">Online</span>
        </div>
        <div class="status-row">
            <span>Backend API</span>
            <span class="pill {backend_class}">{backend_label}</span>
        </div>
        <div class="status-row">
            <span>AI answers</span>
            <span class="pill pending">Pending</span>
        </div>
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
                <div style="color:var(--text-muted); font-size:12px;">
                    {readiness_pct}% configured
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------

st.markdown(
    '<span class="eyebrow">OmniBrain Document Center</span>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-title">Upload your knowledge</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="page-sub">
        Add a PDF securely and prepare it for intelligent document analysis.
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# Upload card
# -------------------------------------------------------------------

st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown("#### Select a PDF document")

file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"],
    label_visibility="collapsed",
    help=f"PDF files up to {MAX_FILE_MB} MB are supported.",
)

st.caption(f"PDF only - Maximum file size: {MAX_FILE_MB} MB")
st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# Validation and FastAPI upload
# -------------------------------------------------------------------

if backend_online:
    st.markdown(
        """
        <div class="banner success">
            <div class="dot"></div>
            <div>FastAPI backend connected. Your document can be uploaded securely.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="banner" style="border-left-color:#ef4444;
             background:linear-gradient(90deg, rgba(239,68,68,0.14),
             rgba(124,58,237,0.06));">
            <div class="dot" style="background:#ef4444;"></div>
            <div>
                Backend API is offline. Start FastAPI at http://127.0.0.1:8000.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
    is_valid, validation_message = validate_pdf(file)

    if not is_valid:
        st.markdown(
            f"""
            <div class="banner" style="border-left-color:#ef4444;
                 background:linear-gradient(90deg, rgba(239,68,68,0.14),
                 rgba(124,58,237,0.06));">
                <div class="dot" style="background:#ef4444;"></div>
                <div>{validation_message}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        file_bytes = file.getvalue()
        file_id = sha256(file_bytes).hexdigest()[:12]
        size_mb = file.size / (1024 * 1024)
        safe_file_name = escape(file.name)

        st.markdown(
            f"""
            <div class="banner">
                <div class="dot"></div>
                <div>
                    <strong>{safe_file_name}</strong> - {size_mb:.1f} MB -
                    ready for upload.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Upload to OmniBrain",
            disabled=not backend_online,
        ):
            progress = st.progress(10, text="Preparing secure upload...")

            try:
                progress.progress(35, text="Sending PDF to FastAPI...")

                response = requests.post(
                    UPLOAD_URL,
                    files={
                        "file": (
                            file.name,
                            file_bytes,
                            file.type or "application/pdf",
                        )
                    },
                    timeout=30,
                )

                progress.progress(80, text="Confirming backend response...")

                if response.status_code == 200:
                    result = response.json()

                    st.session_state.uploaded_file = result.get(
                        "filename",
                        file.name,
                    )
                    st.session_state.processed_document_id = file_id
                    st.session_state.workspace_status = "Ready"

                    if st.session_state.last_uploaded_file_id != file_id:
                        st.session_state.prepared_docs += 1
                        st.session_state.last_uploaded_file_id = file_id

                    progress.progress(100, text="Upload complete.")

                    st.markdown(
                        f"""
                        <div class="banner success">
                            <div class="dot"></div>
                            <div>
                                <strong>Upload successful.</strong>
                                {result.get("message", "Document accepted by OmniBrain backend.")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button("Go to Ask OmniBrain"):
                        st.switch_page("pages/Chat.py")

                else:
                    try:
                        error_detail = response.json().get(
                            "detail",
                            response.text,
                        )
                    except ValueError:
                        error_detail = response.text

                    st.error(
                        f"Upload failed ({response.status_code}): {error_detail}"
                    )

            except requests.ConnectionError:
                st.error(
                    "Cannot connect to FastAPI. Confirm the backend is running "
                    "at http://127.0.0.1:8000."
                )

            except requests.Timeout:
                st.error("The upload request timed out. Please try again.")

            except requests.RequestException as error:
                st.error(f"Upload error: {error}")

            finally:
                progress.empty()


# -------------------------------------------------------------------
# Security note
# -------------------------------------------------------------------

st.markdown(
    """
    <div class="security-note">
        Security note: PDF validation is performed in the frontend before upload.
        The document is then sent to the OmniBrain FastAPI Upload API for
        server-side processing.
    </div>
    """,
    unsafe_allow_html=True,
)
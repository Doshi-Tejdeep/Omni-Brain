import streamlit as st

st.title("📤 Upload Document")

file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if file:
    st.success(f"{file.name} uploaded successfully")

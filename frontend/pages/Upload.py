import streamlit as st
import requests

st.title("📤 Upload Document")

uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file is not None:

    if st.button("Upload"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files
            )

            if response.status_code == 200:
                data = response.json()

                st.success("✅ File uploaded successfully!")

                st.write("**Filename:**", data.get("filename"))

                if "type" in data:
                    st.write("**File Type:**", data["type"])

                elif "content_type" in data:
                    st.write("**File Type:**", data["content_type"])

            else:
                st.error("❌ Upload failed")

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend.")
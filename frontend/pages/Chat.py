import streamlit as st

st.title("💬 Chat")

question = st.chat_input(
    "Ask something about your document..."
)

if question:
    st.write("You asked:", question)
    st.write("AI response will be connected later.")
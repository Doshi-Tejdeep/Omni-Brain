import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="OmniBrain Chat",
    page_icon="🧠",
    layout="wide",
)


def ask_backend(question):
    try:
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"question": question},
            timeout=120,
        )

       if response.status_code == 200:
            data = response.json()

            answer_data = data.get("answer", "")
            sources = data.get("sources", [])

            # Backend may return the RAG result as a nested dictionary
            if isinstance(answer_data, dict):
                answer = answer_data.get("answer", "")
                sources = answer_data.get("sources", sources)
            else:
                answer = answer_data

            # Make absolutely sure Streamlit receives plain text
            if isinstance(answer, dict):
                answer = answer.get("answer", "")

            if not isinstance(answer, str):
                answer = str(answer)

            if not isinstance(sources, list):
                sources = [str(sources)]

            return answer, sources


        return (
            f"Backend error: {response.status_code}",
            [],
        )

    except Exception:
        return (
            "⚠️ Can't reach the backend. Start FastAPI at http://127.0.0.1:8000.",
            [],
        )


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0


st.title("🧠 OmniBrain Chat")
st.caption("Ask questions about your uploaded documents.")


# Display previous conversation
for entry in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(entry["question"])

    with st.chat_message("assistant"):
        st.markdown(
            f'<div class="answer-card">{entry["answer"]}</div>',
            unsafe_allow_html=True,
        )

        if entry.get("sources"):
            with st.expander("Sources"):
                for src in entry["sources"]:
                    st.markdown(f"- {src}")


query = st.chat_input("Ask a question about your document...")

if query:
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = ask_backend(query)

        st.markdown(
            f'<div class="answer-card">{answer}</div>',
            unsafe_allow_html=True,
        )

        if sources:
            with st.expander("Sources"):
                for src in sources:
                    st.markdown(f"- {src}")

    st.session_state.chat_history.append(
        {
            "question": query,
            "answer": answer,
            "sources": sources,
        }
    )

    st.session_state.questions_asked += 1


if st.button("Clear conversation"):
    st.session_state.chat_history = []
    st.session_state.questions_asked = 0
    st.rerun()


st.markdown("---")
st.caption("Your conversation will appear here once you ask a question.")

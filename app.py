
import streamlit as st

from agent import run_agent
from tools import get_all_tasks


st.set_page_config(
    page_title="Small Business AI Agent",
    page_icon="🤖",
)

st.title("🤖 Small Business AI Operations Agent")
st.caption("An AI assistant that manages tasks using PostgreSQL.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation history.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_message = st.chat_input(
    "e.g. Add a task to follow up with a customer"
)

if user_message:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.write(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = run_agent(user_message)
                st.write(result)
            except Exception:
                result = (
                    "Something went wrong. Check that Ollama and "
                    "PostgreSQL are running, and inspect the "
                    "PyCharm terminal for the error."
                )
                st.error(result)

    st.session_state.messages.append(
        {"role": "assistant", "content": result}
    )

# Read the actual database for the sidebar.
with st.sidebar:
    st.subheader("Business task list")

    try:
        tasks = get_all_tasks()

        if tasks:
            for task_id, title, status, created_at in tasks:
                icon = "✅" if status == "completed" else "🕒"
                st.write(f"{icon} **#{task_id}** — {title}")
                st.caption(f"Status: {status}")
        else:
            st.info("No tasks added yet.")

    except Exception as error:
        st.error(f"Could not load tasks: {error}")

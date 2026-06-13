import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from backend.app.feedback_store import save_feedback   # 👈 ADD THIS


def render_chat(messages, thread_id):
    for idx, msg in enumerate(messages):
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.text(msg.content)

        elif isinstance(msg, AIMessage):
            if msg.content:
                with st.chat_message("assistant"):
                    st.text(msg.content)

        elif isinstance(msg, ToolMessage):
            continue


def handle_user_input(chatbot, thread_key, user_input):
    CONFIG = {
        "configurable": {"thread_id": thread_key},
        "metadata": {"thread_id": thread_key},
        "run_name": "chat_turn",
    }

    with st.chat_message("assistant"):
        status_holder = {"box": None}

        def stream():
            for message_chunk, _ in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")

                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        # 🔥 STREAM RESPONSE
        response = st.write_stream(stream())

        # 🔥 Finish tool status
        if status_holder["box"]:
            status_holder["box"].update(
                label="✅ Tool finished",
                state="complete",
                expanded=False,
            )

        # =========================
        # ✅ ADD FEEDBACK BUTTONS
        # =========================

        st.markdown("")  # spacing

        col1, col2 = st.columns([1, 1])

        message_key = f"{thread_key}-{hash(response)}"

        with col1:
            if st.button("👍 Like", key=f"up-{message_key}", use_container_width=True):
                save_feedback(thread_key, message_key, 1)
                st.toast("Thanks for your feedback!")

        with col2:
            if st.button("👎 Dislike", key=f"down-{message_key}", use_container_width=True):
                save_feedback(thread_key, message_key, -1)
                st.toast("Feedback noted!")

    return response
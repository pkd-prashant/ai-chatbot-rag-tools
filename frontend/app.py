import streamlit as st
import uuid

import sys
import os

# Add project root to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from backend.app import (
    chatbot,
    ingest_pdf,
    retrieve_all_threads,
    thread_document_metadata,
)

from sidebar import render_sidebar
from chat_area import render_chat, handle_user_input

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


# ---------- Helpers ----------

def generate_thread_id():
    return str(uuid.uuid4())


def reset_chat():
    st.session_state["thread_id"] = generate_thread_id()
    st.session_state["message_history"] = []


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    return state.values.get("messages", [])


def conversation_title(thread_id):
    messages = load_conversation(thread_id)
    for msg in messages:
        if isinstance(msg, HumanMessage):
            return msg.content[:30] + ("..." if len(msg.content) > 30 else "")
    return "New chat"


# ---------- Session Init ----------

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

if "ingested_docs" not in st.session_state:
    st.session_state["ingested_docs"] = {}


thread_key = st.session_state["thread_id"]
thread_docs = st.session_state["ingested_docs"].setdefault(thread_key, {})
threads = st.session_state["chat_threads"][::-1]


# ---------- Sidebar ----------

def on_new_chat():
    reset_chat()
    st.rerun()


def on_pdf_upload(uploaded_pdf):
    if uploaded_pdf.name not in thread_docs:
        summary = ingest_pdf(
            uploaded_pdf.getvalue(),
            thread_id=thread_key,
            filename=uploaded_pdf.name,
        )
        thread_docs[uploaded_pdf.name] = summary
        st.sidebar.success("PDF indexed")


selected_thread = render_sidebar(
    thread_key,
    thread_docs,
    threads,
    conversation_title,
    on_new_chat,
    on_pdf_upload,
)


# ---------- Main Chat ----------

st.title("AI Assistant")

messages = load_conversation(thread_key)
# render_chat(messages)
render_chat(messages, thread_key)

user_input = st.chat_input("Ask anything")

if user_input:
    with st.chat_message("user"):
        st.text(user_input)

    response = handle_user_input(chatbot, thread_key, user_input)

    st.session_state["message_history"].append(
        {"role": "assistant", "content": response}
    )


# ---------- Thread Switching ----------

if selected_thread:
    st.session_state["thread_id"] = selected_thread
    st.rerun()


# ---------- Footer ----------

doc_meta = thread_document_metadata(thread_key)
if doc_meta:
    st.caption(
        f"Document indexed: {doc_meta.get('filename')} "
        f"(chunks: {doc_meta.get('chunks')}, pages: {doc_meta.get('documents')})"
    )
import streamlit as st

def render_sidebar(
    thread_key,
    thread_docs,
    threads,
    conversation_title_fn,
    on_new_chat,
    on_pdf_upload,
):
    st.sidebar.title("AI Chatbot")

    # ---- New Chat ----
    if st.sidebar.button("New Chat", use_container_width=True):
        on_new_chat()

    # ---- Document Status ----
    if thread_docs:
        latest_doc = list(thread_docs.values())[-1]
        st.sidebar.success(
            f"Using `{latest_doc.get('filename')}` "
            f"({latest_doc.get('chunks')} chunks from {latest_doc.get('documents')} pages)"
        )
    else:
        st.sidebar.info("No PDF indexed yet.")

    # ---- Upload PDF ----
    uploaded_pdf = st.sidebar.file_uploader(
        "Upload a PDF for this chat", type=["pdf"]
    )

    if uploaded_pdf:
        on_pdf_upload(uploaded_pdf)

    # ---- Conversation List ----
    st.sidebar.subheader("Recent conversations")

    selected_thread = None

    if not threads:
        st.sidebar.write("No past conversations yet.")
    else:
        for thread_id in threads:
            title = conversation_title_fn(thread_id)
            if st.sidebar.button(title, key=f"thread-{thread_id}"):
                selected_thread = thread_id

    return selected_thread
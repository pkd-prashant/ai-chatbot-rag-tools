# helper functions used by frontend

from langchain_core.messages import HumanMessage
from .graph import chatbot, checkpointer
from .rag_store import ingest_pdf, thread_document_metadata
from .feedback_store import init_feedback_table
from .feedback_store import save_feedback

init_feedback_table()

def send_message(thread_id: str, user_input: str) -> str:
    config = {
        "configurable": {"thread_id": thread_id},
        "metadata": {"thread_id": thread_id},
        "run_name": "chat_turn",
    }

    output = []
    for message_chunk, _ in chatbot.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config=config,
        stream_mode="messages",
    ):
        if hasattr(message_chunk, "content") and message_chunk.content:
            output.append(str(message_chunk.content))

    return "".join(output)

def load_conversation(thread_id: str):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
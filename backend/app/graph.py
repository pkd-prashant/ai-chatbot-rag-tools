import sqlite3
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from .config import settings
from .core import llm
from .tools import search_tool, get_stock_price, calculator, rag_tool

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# binding llm with tools 
tools = [search_tool, get_stock_price, calculator, rag_tool]
llm_with_tools = llm.bind_tools(tools)

def chat_node(state: ChatState, config=None):
    """LLM node that may answer or request a tool call."""
    thread_id = None
    if config and isinstance(config, dict):
        thread_id = config.get("configurable", {}).get("thread_id")
        
    messages = state["messages"]

    system_prompt = SystemMessage(

        content=(
            "You are a helpful assistant.\n\n"
            "Use tools only when necessary.\n"
            "Available tools:\n"
            "- rag_tool (for PDF questions; include thread_id" + str(thread_id)+")\n"
            "- calculator\n"
            "- get_stock_price\n"
            "- duckduckgo_search\n\n"
            "Rules:\n"
            "- If a PDF is available and the query is about the document, use rag_tool.\n"
            "- If no PDF is available and needed, ask the user to upload one.\n"
            "- Do NOT assume absence of PDF unless explicitly told.\n"
            "- If tool results are returned, interpret them and respond clearly.\n"
            "- Otherwise answer directly.\n"
        )
    )

    response = llm_with_tools.invoke([system_prompt] + messages)

    return {"messages": [response]}

conn = sqlite3.connect(settings.sqlite_path, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

tool_node = ToolNode(tools)

# create graph
graph = StateGraph(ChatState)

# add node
graph.add_node('chat_node', chat_node)
graph.add_node('tools', tool_node)

# add edge
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer = checkpointer)
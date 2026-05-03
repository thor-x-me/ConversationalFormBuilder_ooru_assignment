from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
import form_io_tools

# Augment the LLM with tools
tools = [form_io_tools.create_form, form_io_tools.get_form_data, form_io_tools.get_created_forms, form_io_tools.update_form]
tools_by_name = {tool.name: tool for tool in tools}

model = ChatOllama(model="qwen3.5:latest", keep_alive="1h")
model_with_tools = model.bind_tools(tools)


def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with managing form.io form." \
                        "Do what the user asks while staying generic." \
                        "Use meaingful names that can be identified easily within other forms."
                    )
                ]
                + state["messages"]
            )
        ],
    }


# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm", llm_call)
agent_builder.add_node("tools", ToolNode(tools))

# Add edges to connect nodes
agent_builder.add_edge(START, "llm")
agent_builder.add_conditional_edges(
    "llm",
    tools_condition,
)
agent_builder.add_edge("tools", "llm")
agent_builder.add_edge("llm", END)

# Compile the agent
agent = agent_builder.compile()

message = """**Form Information:**
- **Title:** Name and Mobile Number Collection Form
- **Machine Name:** nameMobileForm
- **URL Path:** name-mobile
- **Form ID:** 69f772f6c4808d5b227f57cc

I can't see any thing in the dropdown of gender box, please fix it.
"""
from langchain.messages import HumanMessage
messages = [HumanMessage(content=message)]


for chunk in agent.stream(
    {"messages": messages},
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        message_chunk, metadata = chunk["data"]
        if message_chunk.content:
            print(message_chunk.content, end="", flush=True)
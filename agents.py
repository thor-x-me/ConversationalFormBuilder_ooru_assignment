from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
import form_io_tools
from form_io import get_form_data
import json

# Augment the LLM with tools
tools = [form_io_tools.create_form, form_io_tools.get_form_data, form_io_tools.get_created_forms, form_io_tools.update_form]

model = ChatOllama(model="qwen3.5:latest", keep_alive="1h")
model_with_tools = model.bind_tools(tools)


async def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    return {
        "messages": [
            await model_with_tools.ainvoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with managing form.io form."
                        "Do what the user asks while staying generic."
                        "Use meaningful names that can be identified easily within other forms."
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


async def stream_agent(messages):
    all_messages = []

    async for msg, metadata in agent.astream(
        {"messages": messages},
        stream_mode="messages"
    ):
        all_messages.append(msg)

        # stream tokens
        if hasattr(msg, "content") and isinstance(msg.content, str):
            yield json.dumps({
                "type": "token",
                "data": msg.content
            }) + "\n"

    # finding form_id so that version canbe added
    for msg in reversed(all_messages):
        if isinstance(msg, ToolMessage) and msg.name == "create_form":
            content = msg.content
            
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except:
                    continue

            form_id = content.get("_id") or content.get("form_id")
            break
    form_data = get_form_data(form_id)
    
    yield json.dumps({
        "type": "form_data",
        "data": form_data
    }) + "\n"
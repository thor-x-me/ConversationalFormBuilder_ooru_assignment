from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from form.agents.tools import create_form, get_created_forms, get_form_data, update_form
# from langgraph.checkpoint.memory import InMemorySaver  

# Augment the LLM with tools
tools = [create_form.create_form, get_form_data.get_form_data, get_created_forms.get_created_forms, update_form.update_form]

model = ChatOllama(model="qwen3.5:latest", keep_alive="1h", reasoning=False)
model_with_tools = model.bind_tools(tools)


async def llm_call(state: MessagesState):
    return {
        "messages": [
            await model_with_tools.ainvoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with managing form.io form."
                        "Do what the user asks while staying generic."
                        "Use meaningful names that can be identified easily within other forms."
                        "If no operation is requested, reply in a friendly tone."
                    )
                ]
                + state["messages"]
            )
        ],
    }

# checkpointer = InMemorySaver()

form_agent = (
    StateGraph(MessagesState)
    .add_node("llm", llm_call)
    .add_node("tools", ToolNode(tools))
    .add_edge(START, "llm")
    .add_conditional_edges(
        "llm",
        tools_condition,
    )
    .add_edge("tools", "llm")
    .add_edge("llm", END)
    .compile()
)

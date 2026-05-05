from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
import form_io_tools
# from langgraph.checkpoint.memory import InMemorySaver  

# Augment the LLM with tools
tools = [form_io_tools.create_form, form_io_tools.get_form_data, form_io_tools.get_created_forms, form_io_tools.update_form]

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

agent = (
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

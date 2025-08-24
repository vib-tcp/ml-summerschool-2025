# LangGraph Basics

LangGraph lets you build reliable, inspectable agent workflows as graphs. You define a typed state, add nodes (functions), connect them with edges, and optionally route conditionally. Tool use is modeled with a dedicated tool node.

## 1) Define the graph state

State is a single object passed between nodes. Keep it explicit and typed.

```python
from typing import List, TypedDict, Annotated
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], "Running chat history"]
    done: bool
```

## 2) Define nodes (functions)

Nodes consume and return the state (partial updates are fine). Here the LLM appends an AI message.

```python
from langchain.chat_models import init_chat_model

def call_llm(state: AgentState) -> AgentState:
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0)
    ai_msg = llm.invoke(state["messages"])  # messages: List[BaseMessage]
    return {"messages": state["messages"] + [ai_msg], "done": False}
```

## 3) Wire edges and compile the graph

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node("llm", call_llm)
workflow.set_entry_point("llm")
workflow.add_edge("llm", END)

graph = workflow.compile()
```

## 4) Conditional edges (routing)

Route based on state. The router returns a key that maps to a next node.

```python
def router(state: AgentState) -> str:
    # Example: stop if the last AI message contains "DONE"
    last = state["messages"][-1]
    text = getattr(last, "content", "")
    return "end" if "DONE" in text else "continue"

workflow.add_conditional_edges(
    "llm",
    router,
    {
        "continue": "llm",  # loop
        "end": END,
    },
)
```

## 5) Tool node

Use a tool node to execute structured tool calls emitted by an LLM.

```python
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

tools = [add]
tool_node = ToolNode(tools)

workflow.add_node("tools", tool_node)

# Typical loop: llm -> (maybe) tools -> llm
def should_call_tools(state: AgentState) -> str:
    last = state["messages"][-1]
    tool_calls = getattr(last, "tool_calls", [])
    return "tools" if tool_calls else "end"

workflow.add_conditional_edges("llm", should_call_tools, {"tools": "tools", "end": END})
workflow.add_edge("tools", "llm")
```

## 6) Invoke the graph

```python
from langchain_core.messages import HumanMessage

inputs = {"messages": [HumanMessage(content="What is 3 + 5? Use tools if needed.")], "done": False}
result_state = graph.invoke(inputs)
final_message = result_state["messages"][-1]
print(final_message.content)
```

That’s the core pattern: typed state, nodes, edges (including conditional routes), a tool node for executing calls, and a compiled graph you can invoke.



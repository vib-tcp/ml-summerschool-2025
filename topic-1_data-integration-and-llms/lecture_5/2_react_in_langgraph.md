# ReAct in LangGraph (End‑to‑End)

We now replicate the ReAct loop—Thought → Action → Observation—using LangGraph. The idea: bind tools to an LLM so it can emit structured tool calls; a tool node executes them; we loop until the model stops calling tools and provides a final answer.

## 1) Define tools

Keep tools small and typed. Here’s a simple calculator.

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

TOOLS = [add, multiply]
```

## 2) State and nodes

We use a messages list as the single source of truth. The agent node calls an LLM that is aware of the tools. The tool node executes any emitted calls and appends tool outputs.

```python
from typing import List, TypedDict, Annotated
from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], "Conversation + traces"]

def agent_node(state: AgentState) -> AgentState:
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0)
    llm_with_tools = llm.bind_tools(TOOLS)
    ai_msg = llm_with_tools.invoke(state["messages"])  # may include tool_calls
    return {"messages": state["messages"] + [ai_msg]}

tool_node = ToolNode(TOOLS)
```

## 3) Routing (continue or stop)

If the latest AI message contains tool calls, go to the tool node; otherwise, stop.

```python
def route_after_agent(state: AgentState) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", []) else "end"
```

## 4) Build the graph

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    route_after_agent,
    {"tools": "tools", "end": END},
)

# After tools run, return to the agent for the next Thought
workflow.add_edge("tools", "agent")

graph = workflow.compile()
```

## 5) Run it

```python
inputs = {
    "messages": [HumanMessage(content="What is 3 + 5? Think step by step and use tools if helpful.")]
}

final_state = graph.invoke(inputs)
print(final_state["messages"][-1].content)
```

## How this mirrors ReAct

- The agent node produces Thoughts and decides on Actions (tool calls)
- The tool node executes Actions and yields Observations (tool outputs)
- The loop continues until the agent produces a final answer without further tool calls

This small pattern scales: you can add domain tools, insert verification nodes, or route through specialized subgraphs—all while keeping the traces readable and the control flow explicit.



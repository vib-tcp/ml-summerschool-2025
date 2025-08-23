# Introduction to Model Context Protocol (MCP)

## Table of Contents

1. [Model Context Protocol (MCP): a gentle introduction](#model-context-protocol-mcp-a-gentle-introduction)
2. [Why MCP?](#why-mcp)
3. [Create a minimal MCP server (FastMCP)](#create-a-minimal-mcp-server-fastmcp)
4. [Call the MCP tools from a LangChain + LangGraph agent](#call-the-mcp-tools-from-a-langchain--langgraph-agent)


## Model Context Protocol (MCP): a gentle introduction

MCP is a simple, open protocol that lets AI models securely access tools and data sources through a standard interface. Instead of every app inventing its own way to “wire up” tools, MCP defines how tools are described, discovered, and called, as well as how results and errors are returned. The goal is portability (use the same tool with many model runtimes/agents), safety (typed inputs/outputs), and simplicity (one mental model, multiple transports such as stdio/HTTP/SSE).

- **Docs**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Spec and examples**: [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)

### Why MCP?

- **Vendor‑neutral tools**: you can reuse the same tool with different LLM providers or agent frameworks.
- **Typed I/O**: tools come with schemas so models know how to call them.
- **Composability**: mix MCP tools with other LangChain tools in one agent.

In this short guide, we’ll build a tiny math tool server with MCP and then call it from a LangChain + LangGraph agent. The narrative is intentionally simple: we want the model to answer “What is 3 + 5?” by deciding to call an MCP tool rather than guessing.

## Create a minimal MCP server (FastMCP)

We’ll expose two tools, `add` and `multiply`, over MCP using the stdio transport. Save this as `math_server.py` and run it with Python.

```python
# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    # Expose the server over stdio (simple and reliable for local development)
    mcp.run(transport="stdio")
```

What this gives us:
- The server announces a capability set and a tool registry to clients.
- Each tool has a name, a short description, and typed parameters.
- Any MCP‑aware client (not just LangChain) can discover and call these tools.

## Call the MCP tools from a LangChain + LangGraph agent

Below we connect to the server via stdio, load the exposed tools into LangChain using `langchain_mcp_adapters`, and create a small ReAct agent with your existing `init_chat_model` helper (as used earlier in these materials). The agent will choose when to call `add`.

```python
# client_langchain_mcp.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

# Uses the helper introduced earlier in these notes
from langchain.chat_models import init_chat_model

import dotenv
dotenv.load_dotenv()

#if you run this on a notebook you need the following
#import nest_asyncio
#nest_asyncio.apply()

async def main():
    server_params = StdioServerParameters(
        command="python",
        # IMPORTANT: use the absolute path to your math_server.py
        args=["/absolute/path/to/math_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the MCP connection and discover tools
            await session.initialize()

            tools = await load_mcp_tools(session)

            llm = init_chat_model(
                model="gemini-2.5-flash",
                model_provider="google_genai",
                temperature=0.2,
            )

            agent = create_react_agent(llm, tools)

            # Ask a question that should trigger a call to the `add` tool
            result = await agent.ainvoke({
                "messages": [("user", "What is 3 + 5?")]
            })

            # Show the final answer the agent produced
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
```

### How this works (conceptually)

1. We run an MCP server that exports typed tools over stdio.
2. The client opens a session, initializes the protocol, and loads tools with `load_mcp_tools(...)`.
3. LangGraph’s ReAct agent reasons about the user request and selects one of the MCP tools (e.g., `add`) with appropriate arguments.
4. The tool executes in the server, returns a typed result, and the agent uses it to produce the final answer.

### Tips and troubleshooting

- Use an absolute path for `math_server.py` in `StdioServerParameters`.
- Keep the server running while the client script executes.
- You can mix MCP tools with any other LangChain tools in the same agent.

That’s all you need to get started: define a tool once with MCP, reuse it across models and frameworks, and keep your integration surface clean and portable.

## Call a remote MCP server

In the previous section we saw how we can define a local MCP server. More precisely, we created a script that gets staret and exposes two tools over MCP. In this section we will see how we can call a remote MCP server (e.g. a server running on a remote machine). Crucially, this step leverages a resources called **[BioContext.AI](https://biocontext.ai)** that we recently released in collaboration with other researchers.

The following code will allow us to query programatically the STRING database through the MCP server and retrieve the interactors of TP53 in human.

```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.chat_models import init_chat_model

mcp_server = "https://mcp.biocontext.ai/mcp"

async with streamablehttp_client(mcp_server) as (read, write, _):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        tools = await load_mcp_tools(session)

        #we subset only on the tools from string
        string_tools = [tool for tool in tools if "string" in tool.name]

        #define the llm
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

        #bind the tools to the llm
        llm_with_tools = llm.bind_tools(string_tools)

        #invoke the llm
        res = await llm_with_tools.ainvoke("What are the iteractors of TP53 in human?")

        #obtain the tool calls
        tool_calls = res.tool_calls

        #execute the tool calls
        tool_results = []
        for call in tool_calls:
            name = call["name"]
            args = call.get("args", {})
            for tool in string_tools:
                if tool.name == name:
                    result = await tool.ainvoke(args)
                    print(result)
```


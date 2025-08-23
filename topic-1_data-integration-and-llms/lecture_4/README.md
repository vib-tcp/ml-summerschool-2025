# Lecture 4: Tool Use and Model Context Protocol (MCP)

## Overview

This lecture introduces how to supercharge Large Language Models (LLMs) with external tools and the Model Context Protocol (MCP). You will start with first principles (having a model emit structured calls to simple Python functions), then move to LangChain’s native tool interface, and finally learn how MCP standardizes tool definitions so they can be reused across models and agent frameworks.

## Learning Objectives

By the end of this lecture, students will be able to:

- Understand why tools are needed to overcome LLM limitations (knowledge cutoff, precision)
- Prompt a model to emit strict JSON for tool invocation and safely parse it
- Define Python tools with LangChain’s `@tool` decorator and bind them to an LLM
- Execute tool calls emitted by an LLM and return results for final synthesis
- Explain MCP concepts (typed tools, transports, client/server separation)
- Build a minimal MCP server (FastMCP) and call it from a LangChain + LangGraph agent
- Connect to a remote MCP server and selectively load and execute tools

## Lecture Materials Index

### 1. Introduction to Tools
**📁 File:** [`0_introduction_to_tools.md`](0_introduction_to_tools.md)

Ground-up approach to tool use: describe Python functions, expose their signatures to the model, and require strict JSON outputs that match the tool’s parameters.

**Key Topics:**
- Why tools: access to fresh knowledge and precise computation
- Describing functions (docstrings, signatures) to the model
- Building a system prompt with a tool registry and JSON schema
- Parsing model outputs into executable calls and returning results

---

### 2. Using LangChain Tools
**📁 File:** [`1_langchain_tools.md`](1_langchain_tools.md)

Define and run tools the idiomatic LangChain way, using a concrete bioinformatics example (`gseapy` enrichment) to demonstrate definition, binding, and execution.

**Key Topics:**
- `@tool` decorator: schema from signature + docstring
- `bind_tools(...)` to declare available tools to the LLM
- Handling `tool_calls` and executing them safely
- Returning tool outputs and prompting the model for final summaries

---

### 3. Introduction to Model Context Protocol (MCP)
**📁 File:** [`2_intro_to_mcp.md`](2_intro_to_mcp.md)

Make tools portable and vendor‑neutral. Create a small FastMCP server that exposes `add` and `multiply`, then call it from a LangChain + LangGraph agent. Also learn how to query a remote MCP server and invoke domain tools.

**Key Topics:**
- What MCP is and why it matters (typed I/O, portability, composability)
- FastMCP server exposing typed tools over `stdio`
- Loading MCP tools into LangChain and using a ReAct agent to call them
- Connecting to a remote MCP server and filtering tools by name

---

## Prerequisites

- Completion of Lecture 2 (LLM APIs and LangChain) and Lecture 3 (Structured Outputs)
- Python 3.9+
- Basic familiarity with JSON, type hints, and virtual environments
- For the enrichment example: `gseapy` and pandas installed
- For MCP examples: MCP Python libraries (`mcp`, `mcp.server.fastmcp`), and optionally `langgraph` and `langchain_mcp_adapters`

## Getting Started

1. **Concepts First:** Read [`0_introduction_to_tools.md`](0_introduction_to_tools.md) and run the simple calculator example end‑to‑end (prompt → JSON → parse → execute).
2. **LangChain Tools:** Implement the `enrichr_query` tool in [`1_langchain_tools.md`](1_langchain_tools.md), bind it to an LLM, and inspect `tool_calls`.
3. **MCP Basics:** Work through [`2_intro_to_mcp.md`](2_intro_to_mcp.md) to build and run the minimal FastMCP server and call it from a LangChain + LangGraph agent.
4. **Remote MCP:** Try the remote MCP example to load domain tools (e.g., STRING) and execute a real query.

## Exercises

- **JSON Tool Caller:** Extend the calculator to support division and robust error handling (bad JSON, missing args, type mismatches). Add retries.
- **Bioinformatics Tool:** Run `enrichr_query` on a custom gene list and have the model summarize the top 10 enriched terms with short rationales.
- **FastMCP Server:** Add a new tool (e.g., `power(a, b)`) to the MCP server and call it via the agent. Log inputs/outputs.
- **Remote MCP:** Connect to a remote MCP endpoint, filter to STRING tools, and retrieve interactors for a gene of your choice.

## Practical Applications

- **Domain Workflows:** Let models call bioinformatics/R&D tools (enrichment, querying knowledge bases) with typed inputs/outputs.
- **Fresh Knowledge Access:** Bridge the knowledge cutoff by calling web/data tools.
- **Operational Reliability:** Keep business logic in Python; let the model orchestrate via tool calls.
- **Portability:** Define once with MCP, reuse across providers and agents.

## Notes on Tool/MCP Capabilities

Different providers offer varying support for tool calls and structured outputs. LangChain abstracts many differences, while MCP standardizes tool description and invocation across runtimes. Prefer typed schemas and explicit argument validation for reliability.

## Course Context

This lecture is part of **Topic 1: Data Integration and LLMs** in the VIB ML Summer School 2025. It builds on structured outputs (Lecture 3) and prepares you to integrate external computation and data sources safely in later lectures.

## Additional Resources

- [LangChain Tools Documentation](https://python.langchain.com/docs/how_to/#tools)
- [LangGraph ReAct Agents](https://langchain-ai.github.io/langgraph/)
- [Model Context Protocol (MCP) Docs](https://modelcontextprotocol.io)
- [MCP GitHub Organization](https://github.com/modelcontextprotocol)
- [gseapy Documentation](https://gseapy.readthedocs.io)



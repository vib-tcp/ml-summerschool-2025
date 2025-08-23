# Using LangChain Tools

## Table of Contents

1. [Using LangChain Tools](#using-langchain-tools)
2. [Define a tool](#define-a-tool)
3. [Bind tools to an LLM](#bind-tools-to-an-llm)
4. [Call the model and execute the tool call](#call-the-model-and-execute-the-tool-call)

## Using LangChain Tools

Large Language Models become significantly more capable when they can call external tools during a conversation. In this short guide, we’ll walk through three key steps using a concrete example:

- Define a tool in LangChain
- Bind the tool to an LLM
- Call the model and execute the tool call it emits

We’ll use an enrichment analysis tool (via `gseapy`) so that a model can analyze a list of genes and retrieve enriched biological processes.

## Define a tool

In LangChain, a Python function becomes a tool by decorating it with `@tool`. The docstring and the function signature help the model understand what the tool does and how to call it. Below we define the `enrichr_query` tool you provided.

```python
from typing import List
from langchain_core.tools import tool
from gseapy import enrichr

@tool
def enrichr_query(gene_list: List[str]):
    """Run enrichment analysis on a list of genes.

    This tool allows to run enrichment analysis on a list of genes using the `gseapy` library.
    Using this tool, a model can get information about the biological processes enriched in a set of genes.

    Args:
        gene_list: list of genes to run enrichment analysis on

    Returns:
        DataFrame: DataFrame containing the enrichment results
    """
    # Run enrichment
    enr = enrichr(
        gene_list=gene_list,
        gene_sets='GO_Biological_Process_2021',
        organism='Human',
        outdir=None,  # no files will be written
        cutoff=0.05
    )

    # Save results as DataFrame
    df_results = enr.results

    return df_results
```

Notes:
- Returning a pandas DataFrame is fine for demos. In production, consider returning a JSON-serializable structure (e.g., `df_results.to_dict(orient="records")`) so tool outputs are easy to transmit and store.

## Bind tools to an LLM

Binding tools tells the model which tools it’s allowed to call and gives it enough schema information to produce structured tool calls (name + arguments). We’ll keep the prompt minimal and use `init_chat_model` for provider-agnostic setup.

```python
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# Create the base model (configure your provider and model ID as needed)
llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

# Bind the tool(s)
llm_with_tools = llm.bind_tools([enrichr_query])

# A simple prompt: system sets expectations; human supplies the input genes
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful bioinformatics assistant. Use tools when needed."),
    ("human", "{question}")
])

chain = prompt | llm_with_tools
```

## Call the model and execute the tool call

When a tool-enabled LLM decides to use a tool, it returns an `AIMessage` that contains one or more `tool_calls`. You are responsible for executing those calls, then (optionally) sending the tool outputs back to the model for a final answer.

```python
# Ask the model to analyze a gene set
user_question = (
    "Please run enrichment on these genes and summarize key biological processes: "
    "TP53, BRCA1, EGFR, MYC, PTEN"
)

ai_msg = chain.invoke({"question": user_question})

# Inspect tool calls (if any)
tool_calls = getattr(ai_msg, "tool_calls", [])
print("Tool calls:", tool_calls)

# Execute each tool call by name with provided arguments
tools_by_name = {enrichr_query.name: enrichr_query}
tool_results = []
for call in tool_calls:
    name = call["name"]
    args = call.get("args", {})
    if name in tools_by_name:
        result = tools_by_name[name].invoke(args)
        tool_results.append({"tool": name, "output": result})

# Optionally, format or reduce the output for readability (e.g., top rows)
if tool_results and hasattr(tool_results[0]["output"], "head"):
    print(tool_results[0]["output"].head(10))
```

If you want the model to produce a final narrative using the tool outputs, send a follow-up message that includes those outputs (or a summarized version) as context. With LangChain, you typically pass tool outputs back as messages and ask the LLM to synthesize a final answer.

```python
from langchain_core.messages import ToolMessage

messages = []
messages.extend(prompt.format_messages(question=user_question))
messages.append(ai_msg)

# Attach tool outputs so the model can read and summarize them
for idx, tr in enumerate(tool_results):
    # Convert complex objects to strings or JSON for reliability
    payload_str = str(tr["output"])  # or json.dumps(...)
    messages.append(
        ToolMessage(content=payload_str, name=tr["tool"], tool_call_id=ai_msg.tool_calls[idx]["id"]) 
    )

final_answer = llm.invoke(messages)
print(final_answer.content)
```

## What we achieved

1. We defined a clear, self-describing tool (`enrichr_query`) that a model can call.
2. We bound the tool to the LLM so it knows the tool’s name and argument schema.
3. We invoked the model, captured its tool call, executed the tool, and (optionally) returned the results for the model to summarize.

This pattern—define tool → bind to LLM → run tool calls—is the core of tool use in LangChain. It keeps your business logic in Python while letting the LLM decide when and how to use it.



# Introduction to Tools

## Table of Contents

1. [Introduction to Tools](#introduction-to-tools)
2. [A simple tool](#a-simple-tool)

## Introduction to Tools

Large Language Models (LLMs) become far more useful when combined with external tools. Tools allow them to overcome key limitations and extend their reasoning capabilities in practical ways:

* **Access to new knowledge**: LLMs have a knowledge cutoff, so tools let them fetch up-to-date or domain-specific information that isn’t in their training data.
* **Task offloading**: Some problems are not easily solved by text-based reasoning; dedicated tools (e.g., calculators, databases, APIs) can handle them more efficiently, much like humans rely on calculators for precise math.

## A simple tool

Every function that takes as input a set of arguments and returns a result can be seen as a tool. However, we must recall that LLMs interact with the world through text, so in order for an LLM to use a tool, we must be able to describe it in text. By using what we learned in the previous lecture, we can try to have a model use two tools: a tool to do additions and a tool to do multiplications. Let us first define a function that adds two numbers together.

```python
def add(a: float, b: float) -> float:
    '''Add two numbers together'''
    return a + b

def multiply(a: float, b: float) -> float:
    '''Multiply two numbers together'''
    return a * b
```

It is important to note how we defined the functions above. We added a docstring to the function that describes what the function does. This would be key to have the model understand what the function does and how to use it.

We can also define a function that takes as input a function and returns a descrpition of it (the docstring and its signature). This will be important in order to have the model understand how to use the tool.

```python
from typing import Callable, List
import inspect

def describe_function(func: Callable) -> str:
    '''Describe a function'''
    desc = f"Function: {func.__name__}\n"
    desc += f"Description: {func.__doc__}\n"
    desc += f"Signature: {inspect.signature(func)}"
    return desc

def describe_functions(funcs: List[Callable]) -> str:
    '''Describe a list of functions'''
    desc = ""
    for func in funcs:
        desc += describe_function(func) + "\n\n"
    return desc
```

Now let us prepare a system prompt that will describe the tools to the model, making it aware of the tools it can use. In order to do so we need to make sure that the model writes a JSON object matching the signature of the function it wants to use. This is a quite involved task and we need some helper functions to do so. These are not really important (since later we will introduce a more general approach to this problem), but it is good to know how to do it.

```python
def _param_spec(func: Callable) -> List[dict]:
    sig = inspect.signature(func)
    hints = get_type_hints(func)
    specs = []
    for name, p in sig.parameters.items():
        typ = hints.get(name, str)
        specs.append({
            "name": name,
            "type": getattr(typ, "__name__", str(typ)),
            "required": p.default is inspect._empty,
            "default": None if p.default is inspect._empty else p.default,
        })
    return specs

def build_tools_block(funcs: List[Callable]) -> str:
    lines = []
    for f in funcs:
        params = _param_spec(f)
        lines.append(f"- {f.__name__}: {f.__doc__ or ''}".strip())
        for p in params:
            default_str = "" if p["required"] else f" (default={p['default']})"
            lines.append(f"    • {p['name']}: {p['type']}{default_str}")
    return "\n".join(lines)

def build_json_schema(funcs: List[Callable]) -> str:
    names = [f.__name__ for f in funcs]
    return json.dumps({
        "type": "object",
        "properties": {
            "tool": {"type": ["string", "null"], "enum": names + [None]},
            "args": {"type": "object"}
        },
        "required": ["tool", "args"],
        "additionalProperties": False
    }, indent=2)

def build_system_prompt(funcs: List[Callable]) -> str:
    tools_block = build_tools_block(funcs)
    schema = build_json_schema(funcs)
    examples = [
        {"tool": "add", "args": {"a": 1, "b": 2}},
        {"tool": "multiply", "args": {"x": 3, "y": 4}},
    ]
    examples_str = "\n".join(json.dumps(e, indent=2) for e in examples)
    return f"""You can call Python tools by emitting exactly ONE JSON object with this shape:

- tool: one of the tool names below (or null if no tool is needed)
- args: an object whose keys match the tool's parameters exactly

TOOLS AVAILABLE:
{tools_block}

OUTPUT FORMAT (STRICT):
Return ONLY a JSON object, no prose, no code fences.

Call object schema (guidance):
{schema}

EXAMPLES (strict JSON, no extra text):
{examples_str}

If you do NOT need any tool, append to the end of the response:
{{"tool": null, "args": {{}}}}
"""
```

We can try now to see one example of system prompt.

```python
funcs = [add, multiply]
system_prompt = build_system_prompt(funcs)
print(system_prompt)
```

We can now invoke the model with the system prompt we just prepared.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("human", "{input}")
]).partial(system_prompt=system_prompt)

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
chain = prompt | llm

msg = chain.invoke({"input": "What is 1 + 2?"})
raw = msg.content 
```

As we recall from the previous lecture, the model will return a string. We need to parse it to get the JSON object.

```python
import json as _json
registry = {f.__name__: f for f in funcs}
call = _json.loads(raw)
result = registry[call["tool"]](**call["args"]) if call["tool"] else None
print("Result:", result)
```

If everything went well, we should have the result of the operation. In the next section we will see how to do this in a more general way with LangChain.


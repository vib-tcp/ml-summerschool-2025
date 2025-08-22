# Lecture 1 ("theory")
- Next token prediction
- Pre-training
- Instruction tuning (RLHF)
- Post-training (math and tool usage)
- Mixtures-of-experts (MOE)
- Thinking models vs standard models
- Commercial vs "open source models"
- Where to find open models
- Model dimension
- Quantisation
- Where to find closed models
- Some questions/suggestions to reflect on possible projects

# Lecture 2 (Inference)
- Setting up together the environment with uv and the right libraries;
- Getting a free API key for Gemini
- Very brief introduction to LangChain and how it can be used to call models
	* setting the ENV variable for API keys
	* init_chat_model
	* human, AI and system messages (concept of conversation template)
	* invoke method and dissecting its output (content, tokens, status)
	* some example of a chain in langchain (?)
- Extending LangChain to use OpenRouter models
	* Get open router API key
	* Get a LangChain-like interface for OpenRouter
	* Show how we can call free models for there
- Local inference with ollama
	* setup in colab (? verify, otherwise a very small local 0.5 should do)
	* do it together on the VIB infrastructure
	* Try the small model
- Show how to call ollama from LangChain
- Anatomy of a system prompt (the example of Biomni)

# Lecture 3 (Structured outputs)
- Reflection on how classical code is structured
- Have the model write an output in JSON format and write a dedicated parser to extract it
- Introduction to Pydantic models (a few examples, show types, and the field decorator)
- Show how to use LangChain to get structured outputs automatically:
	* with_structured
	* using the Pydantic template validator (more general)
- Controlled generation with guidance

# Lecture 4 (Tool usage)
- Some reference on tools (https://arxiv.org/pdf/2305.15334)
- Simple example with the weather (the classical one)
- Exposing a tool to the LLM from a conceptual point of view (docstring and signature)
- Trying to call a function from scratch (explain to the model what the tool does and how it should call it. Parse the output and try to call the tool. We have an example prompt in BioChatter)
- A tool in LangChain + tool binding
- Invoking the tool with the result from the model
- An example of a helpful tool (re-use the example from BioChatter);
- Introduction to MCP
	* What is its purpose
	* how can be used in Python
- How to attach an MCP server to LangChain (mcp adapter libraries)
- A simple example of a local MCP server (calculator)
- A simple example of a remote MCP (biocontext.AI)

# Lecture 5 (Agents)
- A few words on the agents
- Brief introduction to the ReAct framework 
- Brief introduction to langgraph
	* how to define nodes and edges
	* how to define a conditional edge
	* tool node
	* graph state
	* invoke the graph
- Replicate ReAct in langgraph
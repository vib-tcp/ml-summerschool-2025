# Index

* [What is LangChain?](#what-is-langchain)
* [One-liner init + first invoke](#one-liner-init--first-invoke)
* [Statelessness](#statelessness)
* [Different types of messages](#different-types-of-messages)
* [Dissecting the structure of the response](#dissecting-the-structure-of-the-response)
* [The pipe operator in LangChain](#the-pipe-operator-in-langchain)
* [Reusing prompts with partial() syntax](#reusing-prompts-with-partial-syntax)
* [Conversation memory via `MessagesPlaceholder`](#conversation-memory-via-messagesplaceholder)
* [Swapping providers without refactoring the chains](#swapping-providers-without-refactoring-the-chains)
* [Exercises](#exercises)

## What is LangChain?

LangChain is a **framework for building applications with large language models (LLMs)**. Instead of treating an LLM as a black box that takes a prompt and returns text, LangChain provides a structured way to **connect models with other components** like prompts, memory, external APIs, databases, and tools.

The key ideas are:

* **Unified interface across providers**: You can call models from Google (Gemini), OpenAI, Anthropic, etc., with the same syntax, making it easier to switch providers.
* **Messages and prompts as building blocks**: Instead of writing plain strings, LangChain uses structured message objects (`SystemMessage`, `HumanMessage`, `AIMessage`) and templates (`ChatPromptTemplate`) to standardize conversations.
* **Chains and runnables**: You can link multiple steps—like prompt construction → model call → output parsing—into a **chain**, making LLM workflows more reusable and testable.
* **Memory and placeholders**: LangChain supports injecting **chat history** and **variables** dynamically into prompts, enabling contextual conversations.
* **Extensibility**: Beyond calling models, LangChain is designed to integrate with search engines, knowledge bases, and other tools, letting you build **reasoning-and-action pipelines** like RAG (retrieval-augmented generation) or agent systems.

In short:
LangChain is not just about *talking* to a model—it’s about **orchestrating LLMs together with prompts, context, and external resources** to build reliable applications.

For more information, see the [official documentation](https://python.langchain.com/docs/introduction/?_gl=1*1jrtu3w*_gcl_au*MTY3MTA3NzIuMTc1NTc5MDc2Mw..*_ga*ODA4ODU1NDQ5LjE3NTU3OTA3NjM.*_ga_47WX3HKKY2*czE3NTU4ODc0OTckbzYkZzAkdDE3NTU4ODc0OTckajYwJGwwJGgw).


## One-liner init + first invoke

Let's start with a simple example of how to use LangChain to call a model. The `init_chat_model` function is used to initialize a chat model. The model is picked via the `model` and `model_provider` parameters. The `temperature` parameter is used to control the randomness of the model's output (0.0 is the most deterministic, 1.0 is the most random).

```python
from langchain.chat_models import init_chat_model

# Pick via provider:model string → works across providers
llm = init_chat_model(model="gemini-2.5-flash",
                      model_provider="google_genai",
                      temperature=0.2)

llm.invoke("What is the capital of France?")
```

By using the `invoke` method, we can call the model with a prompt. The model will return a response. `init_chat_model` is a convenience function that allows to initialize different models from different providers with a unified interface. To see the list of supported models, see the [official documentation](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html).


## Statelessness

The model is stateless. This means that each time we call the model, we get a new response. This is useful if we want to get a new response for each request. 

```python
response = llm.invoke("My name is John Doe")
print(response)

response = llm.invoke("What is my name?")
print(response)
```

However, if we want to have a conversation with the model, we need to store the conversation history.

To do this, we can gather the conversation history in a list and pass it to the model.

```python
conversation_history = []

response = llm.invoke("My name is John Doe")
conversation_history.append(response)

response = llm.invoke("What is my name?", conversation_history)
print(response)
```

An immidiate consequence of this behavior is that everytime that we call the model, if we want to retain the conversation history, all of the previous messages need to be passed to the model. This means that the cost of each request will increase rapidly as the number of messages in the conversation history increases (we will have more and more tokens in the request). 


## Different types of messages

LangChain provides different types of messages. The most common are:

* `SystemMessage`: A message for setting the overall behavior of the model (the system prompt)
* `HumanMessage`: A message from the human.
* `AIMessage`: A message from the model (format used by the model to answer to the human message).

It is particularly important to flag the messages in the correct way since, during training, the model was trained to recognize the different types of messages. **Multiple type of chat template exist** and usually the right format is described in the documentation of the model. Usually langchain automatically uses the correct template based on the model provider.

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# helpful assistant
system_message = SystemMessage(content="You are a helpful assistant.")
human_message = HumanMessage(content="What is the capital of France?")
resp=llm.invoke([system_message, human_message])
print(resp)

#pirate assistant
system_message = SystemMessage(content="You are always answer like a pirate")
human_message = HumanMessage(content="What is the capital of France?")
resp=llm.invoke([system_message, human_message])
print(resp)

#check the type of all the messages
print(type(system_message))
print(type(human_message))
print(type(resp))
```

## Dissecting the structure of the response

Considering that we still have the response from the previous section, we can dissect the structure of the response.

```python
print("--- CONTENT ---")
print(resp.content)

print("\n--- TOKENS ---")
print(resp.usage_metadata)        # {'input_tokens': ..., 'output_tokens': ..., 'total_tokens': ...}

print("\n--- STATUS/METADATA ---")
print(resp.response_metadata)     # e.g., {'finish_reason': 'STOP', ...}
```

As we can see, the output is not just the text of the response. It contains the content of the response, the usage metadata and the response metadata. Usage metadata is particularly important to understand the cost of the request.

## The pipe operator in LangChain

LangChain provides a pipe operator that allows to chain multiple steps together. This is particularly useful to build a pipeline of steps. We saw that the response from a model is a complex AI message object. There could be cases in which we are interested in extracting only the content of the response. This can be easily achieved by composing dedicated functions with the pipe operator.

Let us consider an example in which we define a **chain** which function is to summarize a given text in a single sentence.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

paragraph = ""#your text here, use wikipedia for example

prompt = ChatPromptTemplate.from_template("You are a helpful assistant that summarizes text in a single sentence. {text}")

chain = prompt | llm | StrOutputParser()

chain.invoke({"text": paragraph})
```

Alternatively, we can use the `from_messages` method to create a prompt template from a list of messages. This is useful in the case in which we want to use a system message to set the overall behavior of the model.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that summarizes text in a single sentence."),
    ("human", "{text}")
])

chain = prompt | llm | StrOutputParser()

chain.invoke({"text": paragraph})
```

## Reusing prompts with `partial()` syntax

We can use the `partial` method to create a new prompt template from a base prompt template. This is useful to reuse the same prompt template with different parameters. In the example below we change the system prompt by adding a specificdomain and a limit to the output.

```python
base = ChatPromptTemplate.from_messages([
    ("system", "You are a domain expert in {domain}. Keep output under {limit} words."),
    ("human", "{question}")
])

bio_prompt = base.partial(domain="bioinformatics", limit="60")
(bio_prompt | llm | StrOutputParser()).invoke({"question": "What is differential expression?"})
```

## Conversation memory via `MessagesPlaceholder`

The `MessagesPlaceholder` is a special placeholder that allows to inject the conversation history into the prompt. This is useful to build chains where the context comes from the conversation history.

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in pharmacology"),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])

history = [
    HumanMessage(content="What is the putative target of venetoclax?"),
    AIMessage(content="The putative target of venetoclax is BCL2.")
]

chain = prompt | llm | StrOutputParser()
chain.invoke({"history": history, "input": "And what about Dabrafenib?"})
```

This tempalate is particualrly useful suited to inject few-shot examples into the prompt.

## Swapping providers without refactoring the chains

As we have seen, defining a chain requires to specify the model provider and the model name. This means that if we want to swap the model provider, we need to refactor the chain. One way to make this process easier is to define a function that creates the chain based on the model provider and the model name.

```python

def make_chain(model_provider: str, model_name: str, temperature: float = 0.2):
    llm = init_chat_model(model=model_name,
                          model_provider=model_provider,
                          temperature=temperature)
    prompt = ChatPromptTemplate.from_template("Give a one‑line TL;DR about {thing}.")            
    return prompt | llm | StrOutputParser()

gemini_25_chain = make_chain("google_genai", "gemini-2.5-flash")
gemini_25_chain.invoke({"thing": "G protein-coupled receptors"})

gemini_20_flash_chain = make_chain("google_genai", "gemini-2.0-flash")
gemini_20_flash_chain.invoke({"thing": "G protein-coupled receptors"})
```

## Exercises

### Exercise 1: Basic Chain Construction (Easy)

Create a simple LangChain pipeline that takes a scientific concept as input and explains it in simple terms suitable for a high school student. Your chain should:

1. Use a `ChatPromptTemplate` with a system message that instructs the model to act as a science teacher
2. Include a human message placeholder for the scientific concept
3. Use the pipe operator to connect the prompt, model, and string output parser
4. Test it with the concept "photosynthesis"

**Expected outcome**: A chain that converts complex scientific terms into simple explanations.

### Exercise 2: Message Types and Conversation (Easy)

Build a conversation scenario where you simulate a dialogue between a patient and a doctor about medication side effects. Your task is to:

1. Create appropriate `SystemMessage`, `HumanMessage`, and `AIMessage` objects
2. Set up the system message to make the model act as a knowledgeable but empathetic doctor
3. Include at least 2 exchanges (human asks about side effects, AI responds, human asks follow-up, AI responds)
4. Use the conversation history to maintain context across the exchanges

**Expected outcome**: A realistic medical consultation dialogue that demonstrates proper message typing and conversation flow.

### Exercise 3: Multi-Specialist Consultation System (Hard)

Create a comprehensive system that allows users to consult with different medical specialists while maintaining conversation history. Your system should demonstrate advanced usage of the concepts covered:

1. Create a base prompt template using `partial()` to generate three different specialist chains (e.g., "cardiology", "oncology", "neurology")
2. Each specialist should have domain-specific behavior defined in the system message
3. Implement `MessagesPlaceholder` to maintain conversation history when consulting with each specialist
4. Create a function similar to `make_chain()` that can generate specialist chains with different domains and model providers
5. Build conversation scenarios where a patient consults multiple specialists, manually switching between them
6. Track and display token usage for each specialist consultation using the response metadata

**Challenge requirements**:
- Create at least 3 different specialist chains using `partial()`
- Demonstrate conversation continuity within each specialist consultation using `MessagesPlaceholder`
- Show how the same patient query gets different responses from different specialists
- Compare token usage across different model providers for the same query
- Manually orchestrate a multi-specialist consultation scenario

**Expected outcome**: A system that showcases advanced prompt templating, conversation memory, and provider flexibility, demonstrating how the same patient case can be handled by different specialists while maintaining conversation context within each consultation.
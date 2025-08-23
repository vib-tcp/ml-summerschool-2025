# Deploying an LLM locally with Ollama

## Table of Contents

1. [Deploying an LLM locally with Ollama](#deploying-an-llm-locally-with-ollama)
2. [Installing Ollama](#installing-ollama)
3. [Using Ollama with LangChain](#using-ollama-with-langchain)
4. [Exercise](#exercise)

## Deploying an LLM locally with Ollama

**Ollama** is an **open-source tool** that lets you **run large language models (LLMs) locally** on your own computer—whether you’re using Windows, macOS, or Linux—without needing to rely on cloud-based services.

Here are some of the main features of Ollama:

* **Privacy & Control:** Since everything runs on your device, your data stays local—offering stronger privacy compared to cloud-hosted models.
* **Efficiency:** Ollama uses techniques like **quantization** to minimize resource consumption, making LLMs viable on consumer-grade hardware .
* **Simplicity:** It provides a **command-line interface (CLI)** (and recently, a **Windows GUI**) that simplifies tasks like pulling, running, and managing models .
* **Cross-Platform & Extensible:** Works across major operating systems and supports integration via APIs and model customizations (like defining prompts or using LoRA fine-tuning) .

> [!WARNING]
> **Hardware Requirements for Local LLM Deployment**
> 
> Deploying LLMs locally effectively requires access to an **NVIDIA GPU** with sufficient **VRAM (video memory)**. Modern LLMs, especially larger variants, can require anywhere from 4GB to 80GB+ of VRAM depending on the model size and quantization level.
> 
> While Ollama can run models on CPU-only systems, the performance will be significantly slower, making it impractical for most use cases beyond basic experimentation.
> 
> This tutorial is meant to introduce the **basics of local deployment**. Once we understand how to deploy models locally, we will explore running LLM jobs on **dedicated HPC (High Performance Computing) infrastructure** where appropriate GPU resources are available.


## Installing Ollama

In the shell of your terminal, you need to run the following command:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Once you finished installing Ollama, we are ready to deploy an LLM using Ollama. A list of models can be
found [here](https://ollama.com/library). For instance, we may want to deploy the GPT-2 model for historic reasons. It only has a size of 328 MB, and interacting with it is fast, but quite different from the commercial models available today. Give it a try:

```bash
ollama run mapler/gpt2
```

See if you can get the model to explain to you what the key messages of the 2017 paper "Attention is all you need" are. Or how it responds to you saying "Hi!".

> [!TIP]
> For understanding the difference between legacy models like GPT-2 and the
> conversational style of current models, we can look into advances in
> *instruction fine-tuning* and *reinforcement learning from human feedback*;
> see for example this [IBM blog post](https://www.ibm.com/topics/instruction-tuning).

We can now compare it with the lastest version of the small qwen3 model. This 0.6billion parameter model only has a size of 523 MB, and interacting with should be fast
Also this model is quite different from SOTA commercial models available today but should deliver different results. Give it a try:

```bash
ollama run qwen3:0.6b
```

If we want to deploy a current state-of-the-art model, we can use the newly (smaller) released
version of `gpt-oss`:

```bash
ollama run gpt-oss
```

Without specifying the exact model variant, Ollama will deploy the default for
this model. I encourage you to try the same queries as with the GPT-2 model and
see how the responses differ.

When you're done chatting, you can type `/bye` to exit from the running chat session.

> [!TIP]
> As an exercise, find out which exact model variant is deployed by default
> (size, quantisation, etc.).

## Using Ollama with LangChain

The LangChain library provides a wrapper for Ollama that allows you to use Ollama as
the backend for LLM calls. In order to use it, you need to serve the model as shown so far.
Once you have done that, you can use the `init_chat_model` with a set of proper arguments
to tell LangChain how to connect to the model.

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(model="qwen3:0.6b",
                      model_provider="ollama",
                      temperature=0.2)

llm.invoke("What is the capital of France?")
```

## Exercise

Which differences do you spot between `gpt2`, `gpt-oss` and `qwen3:0.6b`?

Further questions to consider:

- What are the effects of model size on model behaviour, deployment time, and
inference speed?

- What are the effects of model quantisation on model behaviour, deployment
time, and inference speed?

- What is the behavioural difference between completion models like GPT-2 and
instruct-tuned models like `qwen3:0.6b`?

Feel free to experiment with different models and see how they behave; or, if
you are interested in other deployment options.
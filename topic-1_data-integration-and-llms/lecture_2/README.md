# Lecture 2: LLM APIs, Frameworks, and Local Deployment

## Overview

This lecture provides a comprehensive introduction to working with Large Language Models (LLMs) through APIs and frameworks. Students will learn how to set up development environments, work with different model providers, use LangChain for structured LLM interactions, and deploy models locally. The lecture emphasizes practical, hands-on experience with modern LLM tools and frameworks.

## Learning Objectives

By the end of this lecture, students will be able to:

- Set up a modern Python development environment using UV
- Obtain and use API keys for commercial LLM providers (Google Gemini, OpenRouter)
- Build structured LLM applications using LangChain framework
- Deploy and interact with LLMs locally using Ollama
- Understand the anatomy and importance of system prompts in LLM applications

## Lecture Materials Index

### 1. Environment Setup
**📁 File:** [`0_setting_up_uv.md`](0_setting_up_uv.md)

Learn to set up a modern Python development environment using UV, a fast, all-in-one Python package manager. This foundation is essential for all subsequent work with LLM frameworks.

**Key Topics:**
- What is UV and why use it
- Installation across different platforms
- Project initialization and dependency management
- Virtual environment management
- Python version control

**Exercise:** Create a new project with Python 3.11 and install data science dependencies (pandas, numpy, matplotlib, seaborn)

---

### 2. API Access - Google Gemini
**📁 File:** [`1_getting_gemini_API_key.md`](1_getting_gemini_API_key.md)

Get started with commercial LLM APIs by obtaining and configuring access to Google's Gemini models, which offer generous free tiers for learning and development.

**Key Topics:**
- Gemini API rate limits and quotas
- API key generation process
- API verification using curl
- Environment variable configuration

**Exercise:** Set up `.env` file with Gemini API key

---

### 3. LangChain Framework
**📁 File:** [`2_inference_with_langchain.md`](2_inference_with_langchain.md)

Master the LangChain framework for building structured LLM applications. This is the core technical content of the lecture, covering everything from basic model calls to complex conversational systems.

**Key Topics:**
- LangChain philosophy and architecture
- Unified interface across LLM providers
- Message types (System, Human, AI)
- Chains and the pipe operator
- Prompt templates and reusability
- Conversation memory with MessagesPlaceholder
- Provider-agnostic development

**Exercises:**
- **Easy:** Basic chain construction for science education
- **Easy:** Multi-turn medical consultation dialogue
- **Hard:** Multi-specialist consultation system with conversation memory

---

### 4. Alternative Providers - OpenRouter
**📁 File:** [`3_extension_to_openrouter.md`](3_extension_to_openrouter.md)

Expand your toolkit by accessing multiple LLM providers through OpenRouter, which provides a unified OpenAI-compatible API for dozens of different models.

**Key Topics:**
- OpenRouter platform overview
- Account setup and API key generation
- Custom LangChain integration using OpenAI compatibility
- Working with free models

**Technical Implementation:** Custom `ChatOpenRouter` class extending LangChain's `ChatOpenAI`

---

### 5. Local Deployment - Ollama
**📁 File:** [`4_ollama.md`](4_ollama.md)

Learn to deploy and run LLMs locally using Ollama, understanding the trade-offs between cloud and local deployment for privacy, cost, and performance.

**Key Topics:**
- Local LLM deployment benefits and challenges
- Hardware requirements (GPU, VRAM considerations)
- Model comparison (GPT-2 vs. modern instruction-tuned models)
- LangChain integration with local models

**Exercise:** Compare behavior across different model generations and sizes (GPT-2, qwen3:0.6b, gpt-oss)

---

### 6. Advanced Topics - System Prompts
**📁 File:** [`5_anatomy_system_prompt.md`](5_anatomy_system_prompt.md)

Explore advanced prompt engineering through real-world examples, understanding how system prompts guide model behavior in production applications.

**Key Topics:**
- System prompt design principles
- Case study: Biomni agent system prompt
- Industry practices for prompt engineering

**Activity:** Analyze the Biomni agent prompt from the research paper

---

## Prerequisites

- Basic Python programming knowledge
- Familiarity with command-line interfaces
- Understanding of virtual environments (helpful but not required)

## Required Tools

- Python 3.11+
- UV package manager
- Terminal/command prompt access
- Text editor or IDE
- Internet connection for API access

## Getting Started

1. **Start Here:** Begin with [`0_setting_up_uv.md`](0_setting_up_uv.md) to set up your development environment
2. **API Setup:** Follow [`1_getting_gemini_API_key.md`](1_getting_gemini_API_key.md) to get API access
3. **Core Learning:** Work through [`2_inference_with_langchain.md`](2_inference_with_langchain.md) - this is the main content
4. **Expand Your Toolkit:** Explore [`3_extension_to_openrouter.md`](3_extension_to_openrouter.md) for more model options
5. **Local Development:** Try [`4_ollama.md`](4_ollama.md) for offline capabilities
6. **Advanced Concepts:** Read [`5_anatomy_system_prompt.md`](5_anatomy_system_prompt.md) for deeper insights

## Additional Resources

- [LangChain Official Documentation](https://python.langchain.com/docs/introduction/)
- [UV Package Manager Documentation](https://docs.astral.sh/uv/)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [OpenRouter Documentation](https://openrouter.ai/docs/quickstart)
- [Ollama Model Library](https://ollama.com/library)

## Note on Hardware Requirements

Some exercises, particularly those involving local model deployment with Ollama, may require significant computational resources. While CPU-only execution is possible, GPU acceleration (NVIDIA GPU with sufficient VRAM) is recommended for optimal performance.

## Course Context

This lecture is part of **Topic 1: Data Integration and LLMs** in the  VIB ML Summer School 2025. It builds foundational skills for working with LLMs that will be essential for subsequent topics.

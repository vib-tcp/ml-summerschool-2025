# Classical Programming vs. LLM Outputs: A Structural Perspective

## Table of Contents

1. [Structure in Classical Programming](#1-structure-in-classical-programming)
2. [The Challenge of Unstructured LLM Outputs](#2-the-challenge-of-unstructured-llm-outputs)
3. [Why Structure Matters in Production Systems](#3-why-structure-matters-in-production-systems)
4. [LLMs as Text Generators vs. Data Producers](#4-llms-as-text-generators-vs-data-producers)
5. [The Bridge: Prompt Engineering for Structure](#5-the-bridge-prompt-engineering-for-structure)
6. [Trade-offs and Design Decisions](#6-trade-offs-and-design-decisions)

## 1. Structure in Classical Programming

In traditional software development, we work with **well-defined data structures** that provide predictability and type safety. For examples, let us consider the following class one could design to represent a research paper:

```python
# Classical approach: Structured data with clear types
class ResearchPaper:
    def __init__(self, title: str, authors: list[str], year: int, abstract: str):
        self.title = title
        self.authors = authors
        self.year = year
        self.abstract = abstract
        self.validate()
    
    def validate(self):
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if self.year < 1900 or self.year > 2025:
            raise ValueError("Year must be between 1900 and 2025")
        if not self.authors:
            raise ValueError("Must have at least one author")

# Usage is predictable and type-safe
paper = ResearchPaper(
    title="Attention Is All You Need",
    authors=["Vaswani, A.", "Shazeer, N.", "Parmar, N."],
    year=2017,
    abstract="The dominant sequence transduction models..."
)

# We can reliably access structured attributes
print(f"Paper from {paper.year}: {paper.title}")
print(f"Number of authors: {len(paper.authors)}")
```

As we can see this class has a number of **essential characteristics of classical structured data:**

* **Type safety**: Each field has a specific type
* **Validation**: Data constraints are enforced
* **Predictability**: You know exactly what fields exist
* **Error handling**: Clear failure modes when data is invalid


## 2. The Challenge of Unstructured LLM Outputs

LLMs can perform for us a wide range of cognitve task that we might interested in integrating in our applications. However, they naturally generate **free-form text** that humans understand but computers struggle to parse reliably. Consider the following example:

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

# Ask for paper information
response = llm.invoke("""
Extract information about this paper:
"Attention Is All You Need" by Vaswani et al., published in 2017.
It introduced the Transformer architecture for neural networks.
""")

print(response.content)
```

After running the above code, a typical response from the LLM could look something like the following:

```text
This paper, titled "Attention Is All You Need," was authored by Vaswani and colleagues 
in 2017. It's a groundbreaking work that introduced the Transformer architecture, 
which revolutionized neural network design for natural language processing tasks. 
The paper demonstrated that attention mechanisms alone, without recurrence or 
convolution, could achieve state-of-the-art results in machine translation.
```

As we can see, the LLM has generated a text that is not structured in any way. This is a problem because it is not easy to parse this text into a structured format. Crucially we can pinpoint few key issues:

* **Inconsistent format**: Each response might be structured differently
* **Missing fields**: No guarantee all required information is present
* **Extraction complexity**: Need to parse natural language to find data
* **Error-prone**: Typos, variations in formatting, incomplete information
* **No validation**: Can't programmatically verify data correctness


## 3. Why Structure Matters in Production Systems

Many real-world applications need **reliable, parseable data** for several critical reasons. Let us consider a few examples:

### Database Integration

Let us consider a database that we want to populate with the information from the LLM response.

```python
# This won't work with unstructured text
papers_db.insert({
    "title": "???",  # How do we extract this reliably?
    "year": "???",   # What if the LLM says "sometime in 2017"?
    "authors": "???" # How do we split author names correctly?
})
```

### API Responses

As another example, let us consider a REST API that we want to build to serve the information from the LLM response.

```python
# REST APIs need consistent JSON structure
@app.route('/api/papers/<id>')
def get_paper(id):
    paper_info = llm.invoke(f"Get info about paper {id}")
    # Can't return raw LLM text as JSON!
    return jsonify({
        "title": "???",
        "authors": "???",
        "year": "???"
    })
```

### Data Processing Pipelines

Yet another example is a data processing pipeline that we want to build to analyze the information from the LLM response.

```python
# Downstream processing needs predictable structure
def analyze_papers(paper_data_list):
    for paper in paper_data_list:
        # These operations fail with unstructured text
        if paper.year > 2020:  # AttributeError if no .year field
            recent_papers.append(paper)
        
        author_count = len(paper.authors)  # TypeError if authors is a string
        collaborations[paper.title] = author_count
```

### Error Handling and Monitoring
```python
# Production systems need predictable failure modes
try:
    paper = extract_paper_info(llm_response)
    validate_paper(paper)  # Clear validation rules
    save_to_database(paper)
except ValidationError as e:
    logger.error(f"Invalid paper data: {e}")
    metrics.increment('paper_validation_failures')
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    retry_queue.add(paper)
```

---

## 4. LLMs as Text Generators vs. Data Producers

### Traditional View: LLMs as Text Generators

The "traditional" use of LLMs (mostly through their web interface) is to use them as question-answering tools, in a similar fashion to how we use search engines:

```python
# LLM as a text completion tool
prompt = "Write a summary of the paper 'Attention Is All You Need'"
response = llm.invoke(prompt)
# Output: Natural language text for human consumption
```

### Modern View: LLMs as Data Producers/Integrators

However, the modern view of LLMs is that they are not only text generators, but also data producers and integrators. This is achieved by tasking them to produce outputs that can be parsed by computers in computer-readable formats.

```python
# LLM as a structured data extraction tool
prompt = """
Extract paper metadata in JSON format:
{
    "title": "exact title",
    "authors": ["author1", "author2"],
    "year": 2017,
    "abstract": "paper abstract"
}

Paper: "Attention Is All You Need" by Vaswani et al...
"""
response = llm.invoke(prompt)
# Expected output: Valid JSON that can be parsed programmatically
```

This shift in perspective opens up new possibilities and in the next section we will see how we can achive this with bare prompt engineering.

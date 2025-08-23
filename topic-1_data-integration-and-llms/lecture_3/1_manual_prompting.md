# Manual Prompting

## Table of Contents

1. [Obtaining structured data from unstructured text](#obtaining-structured-data-from-unstructured-text)
2. [Using LangChain to design a flexible and robust prompt](#using-langchain-to-design-a-flexible-and-robust-prompt)
3. [Parsing the output](#parsing-the-output)
4. [Few-shot prompting](#few-shot-prompting)

## Obtaining structured data from unstructured text

In this section we will see how we can obtain structured data from unstructured text using the simplest of techniques: bare prompt engineering. Therefore, we will not use any external libraries or tools, but rather we will task directly the LLM to produce the structured data we need.

Let us consider the esiest of the approaches creating a dedicated prompt:

```python
#initialize the LLM
llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

#initialize a mock text
text = """
This paper, titled "Attention Is All You Need," was authored by Vaswani and colleagues 
in 2017. It's a groundbreaking work that introduced the Transformer architecture, 
which revolutionized neural network design for natural language processing tasks. 
The paper demonstrated that attention mechanisms alone, without recurrence or 
convolution, could achieve state-of-the-art results in machine translation.
"""

#define the prompt
prompt = """
<task>
Extract paper information matching this exact JSON schema:
{{
    "title": "string (required)",
    "authors": ["array of strings (required)"],
    "year": "integer between 1900-2025 (required)",
    "abstract": "string (optional)"
}}
</task>

<text>
{text}
</text>
"""

response = llm.invoke(prompt.format(text=text))

print(response.content)
```

>[!NOTE]
> Note the use of the double curly braces `{{` and `}}` to denote the JSON schema. This is a common practice to avoid that `format` method interprets the curly braces as a template to be filled.

>[!TIP]
> Notice how we use **XML-style tags** (`<task>`, `<text>`) to clearly delineate different sections of our prompt. This is a powerful but often unwritten best practice for LLM prompt engineering.


## Using LangChain to design a flexible and robust prompt

We can also re-use what we learned so far about LangChain to design a flexible and robust prompt that can be used to extract the structured data we need.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

task ='''
<task>
You are a helpful assistant that extracts structured data from unstructured text.
You will be given a text about a paper and you should extract information matching this JSON schema:
{{
    "title": "string (required)",
    "authors": ["array of strings (required)"],
    "year": "integer between 1900-2025 (required)",
    "abstract": "string (optional)"
}}
</task>
'''

prompt = ChatPromptTemplate.from_messages([
    ("system", task),
    ("user", "{text}")
])

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"text": text})

print(response)
```

See how we used the `ChatPromptTemplate` to create a prompt template that specifies the extraction task through the system message and the text to be processed through the human message.

## Parsing the output

Let us check however the type of the response obtained from the previous llm

```python
type(response)
```

By running the above code we can see that the response is a string. So, even if the string resembles a JSON object, we still need to parse it to obtain a valid JSON object. To do so we need to define a dedicated function that will extract the JSON object from the string.

```python
import re
import json

def extract_json_blocks(text: str) -> list[dict]:
    """
    Find fenced ```json code blocks and return them as parsed Python objects.
    """
    pattern = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
    results = []
    for match in pattern.finditer(text):
        try:
            results.append(json.loads(match.group(1)))
        except json.JSONDecodeError:
            pass  # skip invalid JSON
    return results
```
By inspecting the signature of the function we see that the function receives as input a string (the response from the LLM) and returns a list of dictionaries (the JSON objects). Therefore, to get our JSON object we need to run:

```python
print(extract_json_blocks(response)[0])
```

## Few-shot prompting

While the previous approaches work well, we can significantly improve the model's performance and consistency by providing examples of the desired input-output format. This technique is called **few-shot prompting**. Let's enhance our LangChain-based approach to include examples:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

system_message = '''
You are a helpful assistant that extracts structured data from unstructured text.
You will be given a text about a paper and you should extract information matching this JSON schema:
{{
    "title": "string (required)",
    "authors": ["array of strings (required)"],
    "year": "integer between 1900-2025 (required)",
    "abstract": "string (optional)"
}}
'''

# Create a prompt template with few-shot examples using multiple messages
prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    
    # Example 1: Human input
    ("user", "The paper 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding' by Devlin, Chang, Lee, and Toutanova was published in 2018. It introduced a new method for pre-training language representations."),
    
    # Example 1: Assistant response
    ("assistant", '''```json
{{
    "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
    "authors": ["Devlin", "Chang", "Lee", "Toutanova"],
    "year": 2018,
    "abstract": "It introduced a new method for pre-training language representations."
}}
```'''),
    
    # Example 2: Human input
    ("user", "ResNet, described in the 2016 paper by He et al., introduced residual connections to enable training of very deep networks. The full title is 'Deep Residual Learning for Image Recognition'."),
    
    # Example 2: Assistant response
    ("assistant", '''```json
{{
    "title": "Deep Residual Learning for Image Recognition",
    "authors": ["He"],
    "year": 2016,
    "abstract": "Introduced residual connections to enable training of very deep networks."
}}
```'''),
    
    # The actual query
    ("user", "{text}")
])

chain = prompt | llm | StrOutputParser()

# Test with our original text
response = chain.invoke({"text": text})
print(response)

# Parse the JSON output
extracted_data = extract_json_blocks(response)[0]
print("Extracted data:", extracted_data)
```

### Benefits of few-shot prompting

1. **Improved consistency**: Examples show the model exactly what format you expect
2. **Better handling of edge cases**: Examples can demonstrate how to handle missing information
3. **Reduced ambiguity**: Clear examples eliminate guesswork about output format
4. **Enhanced accuracy**: Models perform better when given concrete patterns to follow


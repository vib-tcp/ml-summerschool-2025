# Pydantic Fundamentals for Data Validation

## Table of Contents

1. [Introduction to Pydantic](#1-introduction-to-pydantic)
2. [Basic Model Creation](#2-basic-model-creation)
   - [2.1 Essential Field Types](#21-essential-field-types)
   - [2.2 Type Conversion and Behavior](#22-type-conversion-and-behavior)
   - [2.3 Creating Complex Models](#23-creating-complex-models)
3. [Custom Validation](#3-custom-validation)
4. [Field Decorators and Constraints](#4-field-decorators-and-constraints)
   - [4.1 Field Constraints](#41-field-constraints)
   - [4.2 Advanced Field Features](#42-advanced-field-features)

## 1. Introduction to Pydantic

**Pydantic** is a Python library that uses **type annotations** to validate data and parse it into Python objects. It's particularly valuable for LLM applications because it provides a bridge between unstructured text and structured, validated data.

### Why Pydantic for LLM Applications?

Consider the case in which we want to validate the data of a research paper we have extracted from a text. In order to do so we need to define a dedicated function that will validate the data for example:

```python
# Without Pydantic: Manual validation nightmare
def validate_paper_data(data):
    if not isinstance(data.get('title'), str):
        raise ValueError("Title must be a string")
    if not data['title'].strip():
        raise ValueError("Title cannot be empty")
    if not isinstance(data.get('year'), int):
        raise ValueError("Year must be an integer")
    if data['year'] < 1900 or data['year'] > 2025:
        raise ValueError("Year must be between 1900 and 2025")
    # ... many more validations

```

By using Pydantic we can define a cleaner and more coincise dedicated solution:

```python
# With Pydantic: Declarative and automatic
from pydantic import BaseModel, Field
from typing import List

class Paper(BaseModel):
    title: str = Field(..., min_length=1)
    year: int = Field(..., ge=1900, le=2025)
    authors: List[str] = Field(..., min_items=1)

# Usage
paper = Paper(**data)
```

This a approach as several key benefits:
- Automatic validation: Type checking and constraint enforcement
- Clear error messages: Detailed feedback on validation failures
- JSON serialization: Easy conversion to/from JSON
- Documentation: Self-documenting schemas


## 2. Basic Model Creation

### 2.1 Essential Field Types

When building Pydantic models, you'll work with various data types. Think of these types as the building blocks for your data structures. Let's explore each category with practical examples that you might encounter in real applications.

#### Basic Python Types

The foundation of any data model starts with simple, everyday data types:

```python
from pydantic import BaseModel

class UserProfile(BaseModel):
    # Text data - names, descriptions, messages
    username: str           # "john_doe", "alice_wonderland"
    
    # Whole numbers - counts, ages, quantities
    age: int               # 25, 42, 18
    
    # Decimal numbers - prices, measurements, scores
    rating: float          # 4.5, 3.14159, 98.6
    
    # True/False values - flags, permissions, states
    is_active: bool        # True, False

# Example: Creating a user profile
user = UserProfile(
    username="student_2024",
    age=22,
    rating=4.8,
    is_active=True
)
```

#### Working with Dates and Times

Handling temporal data is crucial in most applications. Pydantic makes this straightforward:

```python
from datetime import datetime, date, time

class EventRecord(BaseModel):
    # Full timestamp with date and time
    created_at: datetime    # "2024-01-15T14:30:00" or "2024-01-15 14:30:00"
    
    # Date only (no time information)
    event_date: date       # "2024-01-15"
    
    # Time only (no date information)
    start_time: time       # "14:30:00" or "2:30 PM"

# Real-world example: A workshop registration
workshop = EventRecord(
    created_at="2024-01-15T09:30:00",
    event_date="2024-02-01",
    start_time="14:00:00"
)
print(f"Workshop on {workshop.event_date} starts at {workshop.start_time}")
```

#### Collection Types for Multiple Values

When you need to store multiple related items, use collection types:

```python
from typing import List, Dict, Set, Tuple

class ResearchProject(BaseModel):
    # List: Ordered collection (can have duplicates)
    keywords: List[str]              # ["AI", "machine learning", "neural networks"]
    
    # Dictionary: Key-value pairs for structured data
    metadata: Dict[str, str]         # {"funding": "NSF", "status": "active"}
    
    # Set: Unique values only (no duplicates)
    collaborators: Set[str]          # {"Alice", "Bob", "Charlie"}
    
    # Tuple: Fixed-size, ordered collection
    coordinates: Tuple[float, float] # (40.7128, -74.0060) for lat/lng

# Example: Defining a research project
project = ResearchProject(
    keywords=["deep learning", "computer vision", "medical imaging"],
    metadata={"grant_id": "NSF-2024-001", "duration": "3 years"},
    collaborators={"Dr. Smith", "Dr. Johnson", "Dr. Chen"},
    coordinates=(42.3601, -71.0589)  # Boston coordinates
)
```

#### Flexible Types for Variable Data

Sometimes your data can be different types or might not always be present:

```python
from typing import Optional, Union

class FlexibleUserData(BaseModel):
    # Optional: Field might be missing or None
    middle_name: Optional[str] = None    # Can be "Marie" or None
    
    # Union: Field can be one of several types
    user_id: Union[str, int]            # Can be "user_123" or 12345
    
    # Combined: Optional field that accepts multiple types
    phone: Optional[Union[str, int]] = None  # "555-1234", 5551234, or None

# Examples showing flexibility
user1 = FlexibleUserData(user_id="USER001")  # String ID, no middle name or phone
user2 = FlexibleUserData(
    user_id=42,
    middle_name="Elizabeth", 
    phone="555-0123"
)
```

#### Specialized Types for Specific Use Cases

Pydantic also supports specialized types for common scenarios:

```python
from decimal import Decimal
from uuid import UUID
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Transaction(BaseModel):
    # UUID: Universally unique identifier
    transaction_id: UUID           # "123e4567-e89b-12d3-a456-426614174000"
    
    # Decimal: Precise decimal calculations (important for money!)
    amount: Decimal               # "99.99" - no floating point errors
    
    # Enum: Restricted set of allowed values
    status: PaymentStatus         # Must be one of the enum values

# Example: Creating a financial transaction
payment = Transaction(
    transaction_id="123e4567-e89b-12d3-a456-426614174000",
    amount="149.99",  # String to avoid floating point precision issues
    status=PaymentStatus.COMPLETED
)
```

#### Why These Types Matter

Each type serves a specific purpose:

- **Validation**: Pydantic ensures your data matches the expected type
- **Documentation**: Types make your code self-documenting
- **IDE Support**: Better autocomplete and error detection
- **API Integration**: Clear contracts when working with external systems
- **LLM Applications**: Structured outputs that language models can reliably generate

### 2.2 Type Conversion and Behavior

One of Pydantic's most helpful features is its ability to intelligently convert between compatible types. This means you don't always need to worry about having data in the exact right format - Pydantic will try to convert it for you in sensible ways.

#### Automatic Type Conversion in Action

Let's see how Pydantic handles common conversion scenarios:

```python
from datetime import date
from typing import Annotated

from pydantic import BaseModel, BeforeValidator

# Reusable type: "anything" -> str
StrFromAny = Annotated[str, BeforeValidator(lambda v: str(v))]

class SmartConverter(BaseModel):
    user_id: StrFromAny     # 12345 -> "12345"
    age: int                # "25" -> 25
    score: float            # "87.5" -> 87.5
    is_verified: bool       # "true","1","yes","on" -> True
    birth_date: date        # "2002-03-15" -> date(2002,3,15)

form_data = {
    "user_id": 98765,
    "age": "22",
    "score": "94.7",
    "is_verified": "true",
    "birth_date": "2002-03-15",
}

user = SmartConverter(**form_data)
print(f"User ID: {user.user_id} (type: {type(user.user_id).__name__})")
print(f"Age: {user.age} (type: {type(user.age).__name__})")
print(f"Verified: {user.is_verified} (type: {type(user.is_verified).__name__})")
print(f"Birth date: {user.birth_date} (type: {type(user.birth_date).__name__})")
```

#### Boolean Conversion Rules

Pydantic is quite flexible with boolean values, which is especially useful when working with different data sources:

```python
from typing import Annotated
from pydantic import BaseModel, BeforeValidator

def to_bool(v):
    if v == "":
        return False
    return v

BoolFlex = Annotated[bool, BeforeValidator(to_bool)]

class BooleanExamples(BaseModel):
    setting1: BoolFlex
    setting2: BoolFlex
    setting3: BoolFlex
    setting4: BoolFlex

# All of these evaluate to True
true_examples = BooleanExamples(
    setting1="true",      # String "true"
    setting2=1,           # Number 1
    setting3="yes",       # String "yes"  
    setting4="on"         # String "on"
)

# All of these evaluate to False
false_examples = BooleanExamples(
    setting1="false",     # String "false"
    setting2=0,           # Number 0
    setting3="no",        # String "no"
    setting4=""           # Empty string
)
```

#### When Conversion Fails

Not all conversions are possible. Pydantic will raise clear errors when it can't convert data:

```python
from pydantic import ValidationError

class StrictTypes(BaseModel):
    number: int
    decimal: float

try:
    # This will fail - can't convert "hello" to a number
    invalid = StrictTypes(number="hello", decimal="world")
except ValidationError as e:
    print("Conversion failed:")
    for error in e.errors():
        field = error['loc'][0]
        message = error['msg']
        print(f"  - {field}: {message}")
```

#### Why This Matters for LLM Applications

When working with language models, you often receive data as text (JSON strings). Pydantic's conversion capabilities mean you can:

1. **Accept flexible input**: LLMs might format numbers as strings
2. **Handle variations**: Different date formats from different sources
3. **Reduce preprocessing**: Less manual data cleaning needed
4. **Focus on logic**: Spend time on your application, not data conversion

This automatic conversion makes Pydantic particularly valuable when processing LLM outputs, where the exact format might vary but the intent is clear.

### 2.3 Creating Complex Models

Pydantic allows also to create more complex models by nesting models inside other models. Let us see an example using again the case of a research paper. Let us start by defining a simple model for an author:

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Author(BaseModel):
    name: str
    email: Optional[str] = None
    affiliation: Optional[str] = None
```

We can now create a more complex model for a research paper by nesting the `Author` model inside the `ResearchPaper` model:

```python
class ResearchPaper(BaseModel):
    title: str
    authors: List[Author]
    year: int
    abstract: str
    keywords: List[str]
    published_date: Optional[datetime] = None
```

Let us now instantiate both models:

```python
# Creating instances
author1 = Author(name="John Doe", email="john@university.edu")
author2 = Author(name="Jane Smith", affiliation="MIT")

paper = ResearchPaper(
    title="Attention Is All You Need",
    authors=[author1, author2],
    year=2017,
    abstract="This paper introduces the Transformer...",
    keywords=["transformer", "attention", "neural networks"]
)

print(paper.title)  # Access fields normally
print(paper.model_dump())  # Convert to dictionary
print(paper.model_dump_json())  # Convert to JSON string
```

## 3. Custom Validation

Pydantic allows also to define custom validation rules for the fields of the model. Let us see an example:

```python
from pydantic import BaseModel, field_validator, ValidationError

class Paper(BaseModel):
    title: str
    year: int
    journal: str
    impact_factor: float

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip().title()  # Clean and format
    
    @field_validator('year')
    def year_must_be_reasonable(cls, v):
        if v < 1900 or v > 2025:
            raise ValueError('Year must be between 1900 and 2025')
        return v
    
    @field_validator('impact_factor')
    def impact_factor_positive(cls, v):
        if v < 0:
            raise ValueError('Impact factor must be positive')
        return v
    
    @field_validator('journal')
    def journal_format(cls, v):
        # Standardize journal names
        journal_mappings = {
            'nature': 'Nature',
            'science': 'Science',
            'cell': 'Cell'
        }
        return journal_mappings.get(v.lower(), v)

```

Validators are defined in the class statement and are defined as methods with the `@field_validator` decorator. The method receives the value of the field as input and returns the validated value.

```python
# Usage
paper = Paper(
    title="  attention is all you need  ",  # Will be cleaned and formatted
    year=2017,
    journal="nature",  # Will be standardized to "Nature"
    impact_factor=42.8
)

print(paper.title)    # "Attention Is All You Need"
print(paper.journal)  # "Nature"
```

## 4. Field Decorators and Constraints

### 4.1 Field Constraints

Certain types of constraints can also be defined using the `Field` decorator. Let us see an example:

```python
from pydantic import BaseModel, Field
from typing import List

class ConstrainedPaper(BaseModel):
    # String constraints
    title: str = Field(..., min_length=5, max_length=200)
    abstract: str = Field(..., min_length=50)
    
    # Numeric constraints
    year: int = Field(..., ge=1900, le=2025)  # ge = greater or equal, le = less or equal
    pages: int = Field(..., gt=0, lt=1000)    # gt = greater than, lt = less than
    impact_factor: float = Field(..., ge=0.0)
    
    # Collection constraints
    authors: List[str] = Field(..., min_items=1, max_items=20)
    keywords: List[str] = Field(default=[], max_items=10)
    
    # Field with description and example
    doi: str = Field(
        ..., 
        description="Digital Object Identifier",
        example="10.1000/182",
        pattern=r"^10\.\d{4,}/.*"  # DOI format validation
    )

# Test constraints
try:
    paper = ConstrainedPaper(
        title="AI",  # Too short - will fail
        abstract="Short abstract",  # Too short - will fail  
        year=1800,  # Too old - will fail
        pages=0,  # Must be greater than 0 - will fail
        authors=[],  # Empty list - will fail
        doi="invalid-doi"  # Doesn't match regex - will fail
    )
except ValidationError as e:
    print("Validation errors:")
    for error in e.errors():
        print(f"- {error['loc'][0]}: {error['msg']}")
```

### 4.2 Advanced Field Features

When building sophisticated data models, you'll need features beyond basic type definitions. This section covers two essential techniques: field descriptions for documentation and default factories for creating safe default values.

#### Understanding Field Descriptions and Default Factories

Field descriptions provide self-documentation for your models, making it clear what each field represents. Default factories allow you to create dynamic default values like empty lists or dictionaries that are created fresh for each instance, avoiding the common Python pitfall of shared mutable defaults.

```python
from pydantic import BaseModel, Field
from typing import List

class AdvancedPaper(BaseModel):
    title: str = Field(..., description="Paper title")
    
    # Field with description explaining its purpose
    email: str = Field(..., description="Corresponding author email")
    
    # Field with default factory - creates a new empty list for each instance
    keywords: List[str] = Field(default_factory=list, description="Research keywords")
    
    # Field with simple default value and description
    publication_year: int = Field(2024, description="Year of publication")
    
    # Field with boolean default and description
    is_open_access: bool = Field(default=False, description="Open access status")
```

#### Practical Application

Here's how field descriptions and default factories work in practice:

```python
from typing import List
from pydantic import BaseModel, Field

class AdvancedPaper(BaseModel):
    title: str = Field(..., description="Paper title")
    email: str = Field(..., description="Corresponding author's email")
    keywords: List[str] = Field(default_factory=list, description="Research keywords")
    publication_year: int = Field(2024, description="Year of publication (default 2024)")
    is_open_access: bool = Field(False, description="Open access flag (default False)")

# Usage demonstrating defaults
json_data = {
    "title": "My Research",
    "email": "author@university.edu",
    "keywords": ["machine learning", "AI", "neural networks"]
    # Note: publication_year and is_open_access will use defaults
}

paper = AdvancedPaper(**json_data)
print(paper.title)             # "My Research"
print(paper.email)             # "author@university.edu"
print(paper.keywords)          # ["machine learning", "AI", "neural networks"]
print(paper.publication_year)  # 2024 (default value)
print(paper.is_open_access)    # False (default value)

# Creating another instance shows default_factory creates new lists
paper2 = AdvancedPaper(title="Another Paper", email="test@example.com")
print(paper2.keywords)  # [] (fresh empty list)

# Modifying one instance doesn't affect the other
paper.keywords.append("deep learning")
print(paper.keywords)   # ["machine learning", "AI", "neural networks", "deep learning"]
print(paper2.keywords)  # [] (still empty - separate list)

# Accessing field information (Pydantic v2: use model_fields and FieldInfo.description)
print(AdvancedPaper.model_fields['title'].description)       # "Paper title"
print(AdvancedPaper.model_fields['keywords'].description)    # "Research keywords"
```

**Key Benefits Demonstrated:**
- **Field Descriptions**: Self-documenting models that explain each field's purpose
- **Default Factory**: Safe creation of mutable defaults (lists, dicts) that don't share references between instances
- **Simple Defaults**: Basic default values for optional fields
- **Documentation**: Descriptions can be accessed programmatically for generating API docs or help text

## Coming up next

In the next part of the lecture we will see how to use Pydantic to validate data from LLMs.




# LangChain Structured Outputs — Pharmacology Edition

## Table of Contents

1. [A pharmacology example](#1-a-pharmacology-example)
   - [Example 1: Drug monograph](#example-1-drug-monograph)
   - [Example 2: Oral vs injectable](#example-2-oral-vs-injectable)
2. [A nested example](#2-a-nested-example)
3. [A more general approach](#3-a-more-general-approach)

## 1. A pharmacology example

### Example 1: Drug monograph

Let us consider the case in which we want to get and parse the information from a drug monograph. Without structured outputs, we would have to manually parse the text and extract the information. This is error prone and requires a lot of code. With structured outputs, we can define a Pydantic model and have LangChain enforce the schema and validation for us. Let us first generate the drug monograph with a LLM:

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
drug = "aspirin"

generation_prompt = '''
<task>
Give me a paragraph with information about {drug}:  
 - name
 - indications
 - contraindications
 - common_adverse_effects
 - adult_dose_mg
 - routes
</task>
'''

response = llm.invoke(generation_prompt.format(drug=drug))
drug_monograph = response.content
```

Now that we have the response, let us parse it with a Pydantic model.

> [!NOTE]
> We could have used constrained generation to directly get the response in the correct format. However, here we break down the problem into smaller steps.
> Notably, this two step process models the case in which we may have knolwedge from an external source in free text (say a pubblication) and we want to parse it into a structured format.

Let us now define a Pydantic model for the response.


```python
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain.chat_models import init_chat_model

class Medication(BaseModel):
    name: str = Field(description="Generic or brand name")
    indications: List[str] = Field(description="Therapeutic indications")
    adult_dose_mg: Optional[float] = Field(None, description="Typical adult dose in mg if applicable")
    routes: List[str] = Field(description="Administration routes, e.g., oral, IV")
```

Now that we have the Pydantic model, we can use and ad hoc method provided by LangChain to constrained the model to generate a response abiding to the Pydantic model. Crucially, this method is called `with_structured_output` and it is available for all the models that support it (you can check [here](https://python.langchain.com/docs/integrations/chat/) the list of models that support it).

```python
structured_llm = llm.with_structured_output(Medication)
parsing_prompt = f"Extract medication info following the schema: {drug_monograph}"
monograph = structured_llm.invoke(parsing_prompt)
print(monograph)
```

### Example 2: Oral vs injectable

Sometimes the same concept appears in different forms (oral vs injectable). A Union lets the LLM choose the appropriate schema at runtime while keeping structure. Lets consider the following example:

```python
from typing import Optional, List, Union
from pydantic import BaseModel, Field

class OralMedication(BaseModel):
    name: str
    dosage_form: str = Field(description="e.g., tablet, capsule")
    dose_mg: Optional[float] = Field(None, description="Per dose in mg")

class InjectableMedication(BaseModel):
    name: str
    concentration_mg_per_ml: Optional[float] = Field(None, description="Strength in mg/mL")
    route: str = Field(description="e.g., IV, IM, SC")

class MedicationWrapper(BaseModel):
    oral: Optional[OralMedication] = None
    injectable: Optional[InjectableMedication] = None

    def check_types(self):
        "returns the type of the medication base on the non none field"
        if self.oral is not None:
            return "oral"
        elif self.injectable is not None:
            return "injectable"
        else:
            return None


flexible_llm = llm.with_structured_output(MedicationWrapper)

oral_text = "Paracetamol 500 mg tablet for pain and fever (oral)."
inj_text = "Ondansetron injection 2 mg/mL, given IV for nausea."

oral = flexible_llm.invoke(f"Extract: {oral_text}")
inj = flexible_llm.invoke(f"Extract: {inj_text}")

print(oral.check_types())
print(inj.check_types())
```


## 2. A nested example

Pharmacology often bundles related fields (dose + route + frequency). Nesting groups these logically. Add simple validators for safety. We keep it to three classes to stay readable.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class DosageInstruction(BaseModel):
    route: str = Field(description="Route, e.g., oral, IV")
    dose_mg: float = Field(description="Dose per administration in mg")
    frequency: str = Field(description="e.g., q8h, once daily")

class Manufacturer(BaseModel):
    name: str = Field(description="Company name")
    country: Optional[str] = Field(None, description="Country of origin")

class Drug(BaseModel):
    name: str = Field(description="Generic name")
    indications: List[str] = Field(description="Therapeutic indications")
    dosage: DosageInstruction = Field(description="Standard adult dosing")
    manufacturer: Manufacturer = Field(description="Manufacturer details")

    @field_validator("dosage")
    def dose_positive(cls, v: DosageInstruction):
        if v.dose_mg <= 0:
            raise ValueError("dose_mg must be > 0")
        return v

drug = "ibuprofen"
drug_text = llm.invoke(generation_prompt.format(drug=drug))

nested_llm = llm.with_structured_output(Drug)
drug = nested_llm.invoke(f"Extract detailed drug profile following the schema: {drug_text}")
```


## 3. A more general approach

The apporach using the `with_structured_output` method is not the only way to get structured outputs from a LLM. Another approach is to use the `PydanticOutputParser` class and extends the possibility to use pydantic classic even for models that do not have the `with_structured_output` method.

```python
from langchain_core.output_parsers import PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=Medication)
```

Se how the parser gets initialized with the pydantic model we defined previously. Then we can get the format instructions from this object and use them to parse the response from the LLM.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract per schema:\n{format_instructions}"),
    ("human", "{text}"),
]).partial(format_instructions=format_instructions)

parsing_llm = prompt | llm | parser

# if `drug_text` is an AIMessage, use .content; otherwise pass the raw string
result = parsing_llm.invoke({"text": drug_text})
print(result)
```

## Exercises

### Exercise 1: Structured output for a dietary supplement
Steps:
- Define a new Pydantic model `Supplement` with fields like: `common_names: List[str]`, `active_components: List[str]`, `uses: List[str]`, `typical_adult_dose_mg: Optional[float]`, `forms: List[str]`.
- Initialize a chat model.
- Generate a short paragraph about a supplement (e.g., "vitamin D3" or "melatonin") covering the fields above.
- Constrain the model with `with_structured_output(Supplement)` and parse the generated text.
- Print and verify the parsed object (types and reasonable values).

### Exercise 2: Union classification for route-specific therapies
Steps:
- Define two new Pydantic models:
  - `TopicalTherapy` with fields like: `name: str`, `formulation: str` (e.g., cream, ointment), `site_of_application: str`.
  - `InhaledTherapy` with fields like: `name: str`, `device_type: str` (e.g., HFA inhaler, DPI), `dose_mcg_per_puff: Optional[float]`.
- Create a Union type `TherapyType = Union[TopicalTherapy, InhaledTherapy]`.
- Prepare two short inputs:
  - Topical example: "Miconazole 2% cream applied twice daily to affected area."
  - Inhaled example: "Albuterol HFA inhaler 100 mcg per puff used for wheeze."
- Use `with_structured_output(TherapyType)` to parse both inputs.
- Print Python types and key fields to confirm correct branch selection.

### Exercise 3: Nested model with basic validation (positive dose)
Steps:
- Define three new Pydantic models:
  - `DosePlan` with fields: `route: str`, `dose_value: float`, `dose_unit: str` (e.g., mg, mL).
  - `ManufacturerInfo` with fields: `name: str`, `country: Optional[str]`.
  - `VaccineProfile` with fields: `name: str`, `indications: List[str]`, `schedule: DosePlan`, `manufacturer: ManufacturerInfo`.
- Add a validator on `VaccineProfile` (or on `DosePlan`) to ensure `dose_value > 0`.
- Initialize a chat model and generate a short paragraph about a vaccine (e.g., "Hepatitis B vaccine" or "Tdap") including name, indications, route, dose with unit, and manufacturer details.
- Use `with_structured_output(VaccineProfile)` to parse the text and print the validated object.
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from typing import Optional, List, Union
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import PydanticOutputParser
import json



# Pick via provider:model string → works across providers
llm = init_chat_model(model="gemini-2.5-flash",
                      model_provider="google_genai",
                      temperature=0.2)


prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a biomedical-AI assistant that interprets predictions from a AI-powered predictive model for clinicians.
You are given a JSON with some information regarding the patient and 2 drugs. In the JSON, you are given:
- Patient ID
- Disease type
- For each drug, you will be given:
    - The drug name
    - The predicted class. This class can be one of three options: 
        - No effect if the drug is predicted as having no effect on treating the patient disease
        - Positive response if the drug is predicted as having a positive effect on treating the patient disease
        - Adverse effects if the drug is predicted as having a negative effect on the patient disease
    - Each predicted class has an associated probability
    - Each predicted class has associated features, that are responsible for the prediction. To reflect the importance of these features on the prediction we have the SHAP values. We have the top positive SHAP values and the top negative SHAP values.

Taking into account this JSON and the information explained above, I want you as a smart biomedical-AI assistant to pick the best of the two drugs. I don't want you to talk about the accuracy of the predicition for more than one sentence.
Once you have  picked the best drug for my patient, I want you to write a small report on the chosen drug, please include both positive an negative points about the drug, make it as straigthforward as possible (a maximum of 10 bullet points in total), and targeted towards clinicians.
After that, please write a short paragraph about the features involved in the decision making process, and look in the litterature for information about the relationship between these features and the disease the patient has."""),
    ("human", "{JSON_input}")
])


paragraph = {
  "MM082": {
    "Disease": "Multiple Myeloma",
    "Drugs": {
      "Lenalidomide_Corticosteroid + IMID": {
        "Predicted_Class": "no_effect",
        "Predicted_Prob": 0.9547447562217712,
        "SHAP": {
          "Top_Positive": [
            {
              "Feature": "Prot_NUDT21",
              "Value": 0.24700665473937988
            },
            {
              "Feature": "Prot_RUVBL2",
              "Value": 0.0914645865559578
            },
            {
              "Feature": "Prot_CTNNA1",
              "Value": 0.07321187853813171
            },
            {
              "Feature": "Prot_NOL6",
              "Value": 0.05411645770072937
            },
            {
              "Feature": "Prot_TRIM28",
              "Value": 0.04787661135196686
            },
            {
              "Feature": "Prot_CUL1",
              "Value": 0.03190836310386658
            },
            {
              "Feature": "Prot_RBM4B",
              "Value": 0.03162224218249321
            },
            {
              "Feature": "Prot_RASA3",
              "Value": 0.028923237696290016
            },
            {
              "Feature": "Prot_SNX9",
              "Value": 0.02808314934372902
            },
            {
              "Feature": "Prot_MANF",
              "Value": 0.026811806485056877
            }
          ],
          "Top_Negative": [
            {
              "Feature": "Prot_AP5Z1",
              "Value": -0.21360288560390472
            },
            {
              "Feature": "Prot_SERPINB6",
              "Value": -0.18836499750614166
            },
            {
              "Feature": "Prot_ACTL6A",
              "Value": -0.07269284129142761
            },
            {
              "Feature": "Prot_DAG1",
              "Value": -0.05008324980735779
            },
            {
              "Feature": "Prot_UNIPROT:Q9NXW2",
              "Value": -0.04398971050977707
            },
            {
              "Feature": "Prot_FBP2",
              "Value": -0.03248339146375656
            },
            {
              "Feature": "Prot_HPS4",
              "Value": -0.028641700744628906
            },
            {
              "Feature": "Prot_SOAT1",
              "Value": -0.02380950003862381
            },
            {
              "Feature": "Prot_SIAE",
              "Value": -0.020670264959335327
            },
            {
              "Feature": "Prot_HLA-B",
              "Value": -0.018923014402389526
            }
          ]
        }
      },
      "Prednisone_Corticosteroid": {
        "Predicted_Class": "no_effect",
        "Predicted_Prob": 0.9630155563354492,
        "SHAP": {
          "Top_Positive": [
            {
              "Feature": "Prot_SCYL1",
              "Value": 0.13524340093135834
            },
            {
              "Feature": "Prot_ADA",
              "Value": 0.08501601219177246
            },
            {
              "Feature": "Prot_SCRN2",
              "Value": 0.08418849110603333
            },
            {
              "Feature": "Prot_MPP1",
              "Value": 0.05830083414912224
            },
            {
              "Feature": "Prot_CLCC1",
              "Value": 0.057101719081401825
            },
            {
              "Feature": "Prot_ICAM3",
              "Value": 0.055060941725969315
            },
            {
              "Feature": "Prot_GATM",
              "Value": 0.03815102577209473
            },
            {
              "Feature": "Cyto_IL15",
              "Value": 0.03718799725174904
            },
            {
              "Feature": "Prot_WDR3",
              "Value": 0.03620968759059906
            },
            {
              "Feature": "Prot_CD3E",
              "Value": 0.03213413432240486
            }
          ],
          "Top_Negative": [
            {
              "Feature": "Prot_RTN2",
              "Value": -0.2484387755393982
            },
            {
              "Feature": "Prot_PGD",
              "Value": -0.12715724110603333
            },
            {
              "Feature": "Prot_RHOC",
              "Value": -0.057847727090120316
            },
            {
              "Feature": "Prot_ALDH1B1",
              "Value": -0.04228834807872772
            },
            {
              "Feature": "Prot_RBM42",
              "Value": -0.018115824088454247
            },
            {
              "Feature": "Prot_HLA-DRA",
              "Value": -0.01672101393342018
            },
            {
              "Feature": "Prot_ARHGAP18",
              "Value": -0.013289976865053177
            },
            {
              "Feature": "Prot_GPNMB",
              "Value": -0.012078801169991493
            },
            {
              "Feature": "Prot_TRIQK",
              "Value": -0.007367526181042194
            },
            {
              "Feature": "Prot_CTSZ",
              "Value": -0.0070403097197413445
            }
          ]
        }
      },
      "Thalidomide_Corticosteroid + IMID": {
        "Predicted_Class": "no_effect",
        "Predicted_Prob": 0.9690818786621094,
        "SHAP": {
          "Top_Positive": [
            {
              "Feature": "Prot_CMTM5",
              "Value": 0.14985670149326324
            },
            {
              "Feature": "Prot_ANXA3",
              "Value": 0.1073228120803833
            },
            {
              "Feature": "Prot_ADA",
              "Value": 0.09336427599191666
            },
            {
              "Feature": "Prot_LRCH4",
              "Value": 0.07067485898733139
            },
            {
              "Feature": "Prot_DENR",
              "Value": 0.06795445084571838
            },
            {
              "Feature": "Prot_VPS16",
              "Value": 0.054585836827754974
            },
            {
              "Feature": "Prot_GLUD1",
              "Value": 0.045237768441438675
            },
            {
              "Feature": "Prot_RPS12",
              "Value": 0.041820332407951355
            },
            {
              "Feature": "Prot_CNP",
              "Value": 0.040000367909669876
            },
            {
              "Feature": "Prot_YTHDC2",
              "Value": 0.03631509840488434
            }
          ],
          "Top_Negative": [
            {
              "Feature": "Prot_UTP18",
              "Value": -0.19441673159599304
            },
            {
              "Feature": "Prot_TXNIP",
              "Value": -0.10141079872846603
            },
            {
              "Feature": "Prot_SSR4",
              "Value": -0.0806729719042778
            },
            {
              "Feature": "Prot_HP",
              "Value": -0.036671996116638184
            },
            {
              "Feature": "Prot_NDUFB1",
              "Value": -0.03547965735197067
            },
            {
              "Feature": "Prot_HPX",
              "Value": -0.03390990570187569
            },
            {
              "Feature": "Prot_UNIPROT:O95396",
              "Value": -0.021261675283312798
            },
            {
              "Feature": "Prot_SRP14",
              "Value": -0.018963176757097244
            },
            {
              "Feature": "Prot_YIF1A",
              "Value": -0.0139157734811306
            },
            {
              "Feature": "Prot_SPTLC2",
              "Value": -0.013098880648612976
            }
          ]
        }
      },
      "Dexamethasone+Bortezomib+Pomalidomide_Proteasome Inhibitor regime": {
        "Predicted_Class": "positive_effect",
        "Predicted_Prob": 0.885675847530365,
        "SHAP": {
          "Top_Positive": [
            {
              "Feature": "Prot_YY1",
              "Value": 0.29476577043533325
            },
            {
              "Feature": "Prot_RHOT2",
              "Value": 0.19768477976322174
            },
            {
              "Feature": "Prot_AFTPH",
              "Value": 0.1350427120923996
            },
            {
              "Feature": "Prot_EIF4E2",
              "Value": 0.09856576472520828
            },
            {
              "Feature": "Prot_UTRN",
              "Value": 0.0938216969370842
            },
            {
              "Feature": "Prot_ALOX5AP",
              "Value": 0.08368617296218872
            },
            {
              "Feature": "Prot_TPP2",
              "Value": 0.07091954350471497
            },
            {
              "Feature": "Prot_AGO1",
              "Value": 0.041629478335380554
            },
            {
              "Feature": "Prot_WASH3P|WASH2P",
              "Value": 0.03657505661249161
            },
            {
              "Feature": "Prot_TRADD",
              "Value": 0.035562969744205475
            }
          ],
          "Top_Negative": [
            {
              "Feature": "Prot_MYO1C",
              "Value": -0.2441149801015854
            },
            {
              "Feature": "Prot_TAP2",
              "Value": -0.07064669579267502
            },
            {
              "Feature": "Prot_RNF113A",
              "Value": -0.05915755033493042
            },
            {
              "Feature": "Prot_DHODH",
              "Value": -0.041181161999702454
            },
            {
              "Feature": "Prot_IGKV3D-20",
              "Value": -0.03929716348648071
            },
            {
              "Feature": "Prot_SLC27A3",
              "Value": -0.03218768537044525
            },
            {
              "Feature": "Prot_C2CD2L",
              "Value": -0.03146705403923988
            },
            {
              "Feature": "Prot_PLXDC2",
              "Value": -0.027738479897379875
            },
            {
              "Feature": "Prot_COG4",
              "Value": -0.02713390812277794
            },
            {
              "Feature": "Prot_U2AF2",
              "Value": -0.026349365711212158
            }
          ]
        }
      }
    }
  }
}



chain = prompt | llm | StrOutputParser()
response = chain.invoke({"JSON_input": paragraph})
print(response)


class GNN_prediction_report(BaseModel):
    patient_ID: Optional[Union[str, int]]  # "555-1234", 5551234, or None
    disease_type: str = Field(description="e.g., Melanoma")
    recomended_drug_name: str = Field(description = "e.g., Pembrolizumab")
    info_on_recommended_drug: str = Field(description = "e.g., Pembrolizumab is a PD-1 inhibitor that has demonstrated significant efficacy in advanced melanoma, improving both progression-free and overall survival. Clinically, it can induce durable responses in a subset of patients. However, its use is associated with immune-related adverse effects, including colitis, hepatitis, pneumonitis, endocrinopathies (such as hypothyroidism or hypophysitis), and less commonly severe dermatologic or neurologic toxicities. Careful monitoring and prompt management of these toxicities are essential during treatment")
    decision_making_process: str 

parser = PydanticOutputParser(pydantic_object=GNN_prediction_report)
format_instructions = parser.get_format_instructions()
prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract per schema:\n{format_instructions}"),
    ("human", "{text}"),
]).partial(format_instructions=format_instructions)

parsing_llm = prompt | llm | parser

# if `drug_text` is an AIMessage, use .content; otherwise pass the raw string
result = parsing_llm.invoke({"text": response})
print(result)


from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
MyEncoder().encode(result)


with open(".json", "w") as f:
    json.dump(MyEncoder().encode(result), f, indent=2)
# prompts/classification_prompt.py

from langchain.prompts import PromptTemplate

classification_prompt = PromptTemplate(
    input_variables=["question"],
    template='''
Clasifica la siguiente consulta del usuario en una de las siguientes categorías:

- seguro
- web_search
- conversación_general
- policy_optimizer

Solo responde con una de las cuatro opciones exactas, sin ninguna explicación adicional.

Consulta:
{question}

Clasificación:
'''
)

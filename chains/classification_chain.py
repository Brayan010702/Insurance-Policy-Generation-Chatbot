# chains/classification_chain.py

from langchain.chains import LLMChain
from config.settings import llm, classification_memory
from prompts.classification_prompt import classification_prompt

# Create the classification chain with its own memory
classification_chain = LLMChain(
    llm=llm,
    prompt=classification_prompt,
    output_key="classification",
    memory=classification_memory  # Separate memory
)

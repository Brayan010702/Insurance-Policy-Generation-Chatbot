# chains/conversation_chain.py

from langchain.chains import ConversationChain
from config.settings import llm, shared_memory
from prompts.conversation_prompt import conversation_prompt

# Create the conversation chain using ConversationChain
conversation_chain = ConversationChain(
    llm=llm,
    memory=shared_memory,
    prompt=conversation_prompt
)

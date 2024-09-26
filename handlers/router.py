# handlers/router.py

from chains.classification_chain import classification_chain
from chains.conversation_chain import conversation_chain
from functions.rag_chain import rag_chain
from functions.web_search_chain import web_search_chain
from functions.policy_optimizer_chain import policy_optimizer_chain

# Router function to direct the question to the appropriate chain
async def router(question: str):
    try:
        # Classify the question using the classification chain
        classification_result = await classification_chain.arun(question=question)
        classification = classification_result.strip().lower()

        # Extract the classification label (ensure it's a single word)
        classification = classification.split('\n')[0].strip()

        # Route based on classification
        if classification == "seguro":
            return await rag_chain(question)
        elif classification == "web_search":
            return await web_search_chain(question)
        elif classification == "policy_optimizer":
            return await policy_optimizer_chain(question)
        else:
            # Use conversation_chain for general conversation
            response = await conversation_chain.arun(
                input=question
            )
            return response
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

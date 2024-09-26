# functions/policy_optimizer_chain.py

from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config.settings import llm, vector_db, shared_memory

# Define the Policy Optimizer chain with memory and context-aware prompt
async def policy_optimizer_chain(question: str):
    # Retrieve relevant documents using MultiQueryRetriever
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(),
        llm
    )

    try:
        # Perform the retrieval
        retrieved_docs = await retriever.ainvoke(question)

        # If no documents are retrieved, return a simple message
        if not retrieved_docs:
            return "No se encontraron documentos relevantes sobre optimización de pólizas."

        # Combine all retrieved documents into a single context
        raw_docs = "\n".join([doc.page_content for doc in retrieved_docs])

        # Retrieve conversation history from global memory (synchronously)
        history = shared_memory.load_memory_variables({"input": question})
        history_text = history.get("chat_history", "")

        # Define the Policy Optimizer Prompt Template
        optimizer_prompt_template = f"""
Eres un asistente de inteligencia artificial especializado en seguros para LATAM llamado Seguritos.
Tu rol principal es proporcionar información útil y precisa a los usuarios, respondiendo de manera clara y concisa a sus consultas.

Además, recuerda la información que el usuario te proporciona durante la conversación para ofrecer respuestas más personalizadas.

Usuario: {question}

Analiza los siguientes documentos y proporciona sugerencias para optimizar las pólizas de seguros, 
como formas de reducir costos o mejorar la experiencia del usuario.

Documentos obtenidos:
{raw_docs}
"""

        # Create the PromptTemplate
        optimizer_prompt = PromptTemplate(
            input_variables=["input"],
            template=optimizer_prompt_template
        )

        # Create the LLMChain for Policy Optimizer with shared memory
        optimizer_chain_instance = LLMChain(
            llm=llm,
            prompt=optimizer_prompt,
            memory=shared_memory
        )

        # Generate the optimized response
        optimized_response = await optimizer_chain_instance.arun(
            input=question
        )

        return optimized_response

    except Exception as e:
        # Handle any errors that occur during the Policy Optimization process
        error_response = f"Ocurrió un error durante la optimización de pólizas: {str(e)}"
        return error_response

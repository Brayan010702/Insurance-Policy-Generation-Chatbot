# functions/rag_chain.py

from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config.settings import llm, vector_db, shared_memory

# Define the RAG chain with memory and context-aware prompt
async def rag_chain(question: str):
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
            return "Lo siento, no se encontraron documentos relevantes para tu consulta."

        # Combine all retrieved documents into a single context
        raw_docs = "\n".join([doc.page_content for doc in retrieved_docs])

        # Retrieve conversation history from global memory (synchronously)
        history = shared_memory.load_memory_variables({"input": question})
        history_text = history.get("chat_history", "")

        # Define the RAG Prompt Template by manually inserting raw_docs
        rag_prompt_template = f"""
Eres un asistente de inteligencia artificial especializado en seguros para LATAM llamado Seguritos.
Tu rol principal es proporcionar información útil y precisa a los usuarios, respondiendo de manera clara y concisa a sus consultas.

Además, recuerda la información que el usuario te proporciona durante la conversación para ofrecer respuestas más personalizadas.


Usuario: {question}

Tienes que convertir los siguientes documentos en una respuesta clara y bien estructurada para el usuario final.
Organiza la información de manera que sea fácil de entender y sigue este formato:

1. Resumen breve de los documentos.
2. Detalles más importantes de cada documento.

Documentos obtenidos:
{raw_docs}
"""

        # Create the PromptTemplate
        rag_prompt = PromptTemplate(
            input_variables=["input"],
            template=rag_prompt_template
        )

        # Create the LLMChain for RAG with shared memory
        rag_chain_instance = LLMChain(
            llm=llm,
            prompt=rag_prompt,
            memory=shared_memory
        )

        # Generate the response by passing required variables
        response = await rag_chain_instance.arun(
            input=question
        )

        return response

    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

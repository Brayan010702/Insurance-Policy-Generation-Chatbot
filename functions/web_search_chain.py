# functions/web_search_chain.py

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults
from config.settings import llm, shared_memory

# Define the web search chain
async def web_search_chain(question: str):
    # Hardcoded list of websites to search over
    websites = [
        "https://www.df.cl/ultimasnoticias",
        "https://www.cmfchile.cl/portal/prensa/615/w3-propertyname-818.html",
        # Add more websites here if needed
    ]

    # Combine site restrictions for the search query
    site_restrictions = " OR ".join([f"site:{website}" for website in websites])
    search_query = f"({site_restrictions}) {question}"

    # Initialize the DuckDuckGo search tool
    search = DuckDuckGoSearchResults(backend="news", hl="es")

    try:
        # Perform the web search with the modified query
        results = await search.arun(tool_input=search_query)

        # Extract and format the top 5 results
        top_results = "\n\n".join([
            f"**Título:** {result['title']}\n**Enlace:** {result['href']}\n**Resumen:** {result['snippet']}"
            for result in results[:5]
        ])

        # Retrieve the conversation history from shared memory (synchronously)
        history = shared_memory.load_memory_variables({"input": question})
        history_text = history.get("history", "")

        # Define the web search prompt
        web_search_prompt_template = f"""
Eres un asistente de inteligencia artificial especializado en seguros para LATAM llamado Seguritos.
Tu rol principal es proporcionar información útil y precisa a los usuarios, respondiendo de manera clara y concisa a sus consultas.

Además, recuerda la información que el usuario te proporciona durante la conversación para ofrecer respuestas más personalizadas.

Usuario: {question}

Resumen de las siguientes noticias obtenidas de la web sobre {question}: 
Concéntrate en las noticias más relevantes, resaltando los detalles específicos:

{top_results}
"""

        # Create the PromptTemplate
        web_search_prompt = PromptTemplate(
            input_variables=["input"],
            template=web_search_prompt_template
        )

        # Create the LLMChain for web search summarization with shared memory
        web_search_summarization_chain = LLMChain(
            llm=llm,
            prompt=web_search_prompt,
            memory=shared_memory  # Ensures that history is managed and included
        )

        # Generate the summarized response by passing required variables
        response = await web_search_summarization_chain.arun(
            input=question  # The user's current question
        )

        return response

    except Exception as e:
        # Handle any errors that occur during the web search
        error_response = f"Error al realizar la búsqueda en la web: {str(e)}"
        return error_response

# handlers/handle_user_query.py

from handlers.router import router

# Main handler for user queries
async def handle_user_query(question: str):
    response = await router(question)
    print(response)
    return response

# main.py

import chainlit as cl
from uuid import uuid4

from handlers.handle_user_query import handle_user_query

# Chainlit events to handle the chat
@cl.on_chat_start
async def on_chat_start():
    session_id = str(uuid4())
    cl.user_session.set("session_id", session_id)
    await cl.Message(content="¡Bienvenido! ¿Cómo puedo ayudarte con tus consultas sobre seguros hoy?").send()

@cl.on_message
async def on_message(message: cl.Message):
    # Send a processing message
    msg = cl.Message(content="Procesando tu solicitud...")
    await msg.send()

    try:
        # Handle the user query and get the response
        response = await handle_user_query(message.content)

        # Update the message with the actual response
        msg.content = response
        await msg.update()
    except Exception as e:
        # Handle any errors by updating the message with the error
        msg.content = f"Ocurrió un error: {str(e)}"
        await msg.update()

@cl.on_chat_end
async def on_chat_end():
    await cl.Message(content="¡Gracias por usar nuestro servicio de asistencia en seguros! Si tienes más preguntas en el futuro, no dudes en volver.").send()

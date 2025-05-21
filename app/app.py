import chainlit as cl
from chatbot import get_model_response

@cl.on_chat_start
async def start():
    # Define um título para o histórico do chat
    await cl.Message(content="Olá! Pode me perguntar qualquer coisa.").send()

@cl.on_message
async def respond(message: cl.Message):
    prompt = message.content
    resposta = get_model_response(prompt)

    await cl.Message(content=resposta).send()

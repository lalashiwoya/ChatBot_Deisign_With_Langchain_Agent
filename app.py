
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from utils import init

@cl.on_chat_start
async def on_chat_start():
    llm, memory = init()


 
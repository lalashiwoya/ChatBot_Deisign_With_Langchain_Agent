
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from utils import init
from llama_index.core import Settings
from api.full_chain import init_full_chain
from langchain.schema.runnable.config import RunnableConfig

@cl.on_chat_start
async def on_chat_start():
    llm, memory = init()
    full_chain = init_full_chain(llm)
    cl.user_session.set("full_chain", full_chain)

@cl.on_message
async def on_message(message: cl.Message):
    full_chain = cl.user_session.get("full_chain")
    elements = []
    actions = []
    res = cl.Message(content="", elements=elements, actions=actions)
    
    async for chunk in full_chain.astream(
        {
            "question": message.content,
            "memory": "test_memo",
             
        },
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        # response.append(chunk)
        await res.stream_token(chunk)
    await res.send()
    
 
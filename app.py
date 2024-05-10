
import chainlit as cl
from langchain_openai import ChatOpenAI
from utils import init_llm, init_memory
from llama_index.core import Settings
from legacy_api.full_chain import init_full_chain
from langchain.schema.runnable.config import RunnableConfig
from utils import read_configs_from_toml
from legacy_api.settings import init_settings, update_user_session
import os

from dotenv import load_dotenv
load_dotenv()

configs = read_configs_from_toml("config.toml")

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    test_username = os.getenv("APP_LOGIN_USERNAME")
    test_password = os.getenv("APP_LOGIN_PASSWORD")
    if (username, password) == (test_username, test_password):
        return cl.User(
            identifier="admin"
        )
    else:
        return None

@cl.on_chat_start
async def on_chat_start():
    initial_settings = init_settings()
    settings = await cl.ChatSettings(initial_settings).send()
    update_user_session(settings)
    llm = init_llm(cl.user_session.get("user_settings").llm_model_name)
    memory = init_memory(llm, max_token_limit=configs['memory']['max_token_limit'])
    # full_chain = init_full_chain(llm)
    
    # cl.user_session.set("full_chain", full_chain)
    cl.user_session.set("memory", memory)
    # cl.user_session.set("llm", llm)

@cl.on_message
async def on_message(message: cl.Message):
    user_settings = cl.user_session.get("user_settings")
    # llm = init_llm(user_settings.llm_model_name)
    full_chain = cl.user_session.get("full_chain")
    # full_chain = cl.user_session.get("full_chain")
    memory = cl.user_session.get("memory")
    
    # print(user_settings.llm_model_name)
    elements = []
    actions = []
    res = cl.Message(content="", elements=elements, actions=actions)
    
    async for chunk in full_chain.astream(
        {
            "question": message.content,
            "memory": memory,
            "user_settings": user_settings,
            "topics": "\n".join(configs["topics"]["topics"])
             
        },
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        # response.append(chunk)
        await res.stream_token(chunk)
    await res.send()
    # memory.chat_memory.add_user_message(message.content)
    # memory.chat_memory.add_ai_message(res.content)
    memory.save_context({"input": message.content}, {"output": res.content})
    
    
 
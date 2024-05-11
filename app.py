
import chainlit as cl
from langchain_openai import ChatOpenAI
from utils import init_llm, init_memory
from api.tools.tool_list import init_tools
from llama_index.core import Settings
from langchain.schema.runnable.config import RunnableConfig
from utils import read_configs_from_toml
from api.settings import init_settings
from api.agent_executor import init_agent
import os
from api.settings import set_user_settings_as_pydantic_model
from langchain.schema.runnable.config import RunnableConfig
from utils import custom_load_memory

from dotenv import load_dotenv
load_dotenv()

configs = read_configs_from_toml("config.toml")
tool_configs = read_configs_from_toml("tool_configs.toml")

tools = init_tools(tool_configs=tool_configs,
                       configs=configs)

@cl.on_settings_update
def update_user_session(settings):
    user_settings = set_user_settings_as_pydantic_model(settings)
    
    if user_settings.llm_model_name:
        print("="*20)
        print(user_settings)
        cl.user_session.set("user_settings", user_settings)
        llm = init_llm(user_settings.llm_model_name)
        agent = init_agent(llm=llm,
                       tools=tools)
        cl.user_session.set("agent", agent)
        

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
    llm = init_llm()
    memory = init_memory(llm, max_token_limit=configs['memory']['max_token_limit'])
    cl.user_session.set("memory", memory)

@cl.on_message
async def on_message(message: cl.Message):
    user_settings = cl.user_session.get("user_settings")
    agent = cl.user_session.get("agent")
    # llm = init_llm(user_settings.llm_model_name)
    # agent = cl.user_session.get("agent")
    # full_chain = cl.user_session.get("full_chain")
    memory = cl.user_session.get("memory")
    
    # print(user_settings.llm_model_name)
    elements = []
    actions = []
    res = cl.Message(content="", elements=elements, actions=actions)
    response = ""
    
    async for chunk in agent.astream({
        "question": message.content,
        "chat_history": custom_load_memory(memory),
        "topics": "\n".join(configs["topics"]["topics"])
    }, config=RunnableConfig(callbacks=[
                                        cl.LangchainCallbackHandler(
        stream_final_answer=True,
    )
                                        ])):
        
        content = chunk['messages'][0].content
        marker = "Final Answer:"
        if marker in content:
            
            response = content.split(marker)[-1].strip()
    memory.save_context({"input": message.content}, {"output": response})
    
    # async for chunk in agent.astream({
    #     "question": message.content,
    #     "chat_history": memory,
    #     "topics": "\n".join(configs["topics"]["topics"])
    # }, config=RunnableConfig(callbacks=[
    #                                     cl.LangchainCallbackHandler(
    #     stream_final_answer=True,
    # )
    #                                     ])):
        
    #     content = chunk['messages'][0].content
    #     marker = "Final Answer:"
    #     if marker in content:
            
    #         response = content.split(marker)[-1].strip()

    # await res.send()
    
        
                    
        
             
        
           
    
    # async for chunk in agent.astream(
    #     {
    #         "question": message.content,
    #         "chat_history": memory,
    #         # "user_settings": user_settings,
    #         "topics": "\n".join(configs["topics"]["topics"])
             
    #     },
    #     config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    # ):
    #     # response.append(chunk)
    #     await res.stream_token(chunk)
    #     print("w"*10)
    #     print(chunk)
    # await res['ouptut'].send()
    # memory.chat_memory.add_user_message(message.content)
    # memory.chat_memory.add_ai_message(res.content)
    # memory.save_context({"input": message.content}, {"output": res.content})
    
    
 
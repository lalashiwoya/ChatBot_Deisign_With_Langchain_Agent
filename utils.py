from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory, ConversationTokenBufferMemory
from langchain_core.memory import BaseMemory
from langchain.chat_models.base import  BaseChatModel
from llama_index.llms.openai import OpenAI
import toml

def init_llm(model_name = "gpt-3.5-turbo"):
    llm = ChatOpenAI(temperature=0, model_name = model_name, streaming = True)
    return llm

def init_llm_for_llama_index(model_name = "gpt-3.5-turbo"):
    llm = OpenAI(temperature=0, model_name = model_name, streaming = True)
    return llm

def init_memory(llm: BaseChatModel, max_token_limit:int = 500):
    # memory = ConversationBufferMemory(return_messages = True)
    memory = ConversationSummaryBufferMemory(return_messages = True,
                                            max_token_limit= max_token_limit,
                                            llm = llm)
    return memory
    


def custom_load_memory(memory: BaseMemory) -> str:
    return str(memory.load_memory_variables({})['history'])

def read_configs_from_toml(path: str) -> dict:
    with open(path, 'r') as toml_file:
        data = toml.load(toml_file)
    return data

 
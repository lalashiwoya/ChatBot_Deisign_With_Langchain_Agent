from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory, ConversationTokenBufferMemory
from langchain_core.memory import BaseMemory
from langchain.chat_models.base import  BaseChatModel
import toml

def init_llm():
    llm = ChatOpenAI(temperature=0, model_name = "gpt-3.5-turbo", streaming = True)
    return llm

def init_memory(llm: BaseChatModel, max_token_limit:int = 500):
    # memory = ConversationBufferMemory(return_messages = True)
    memory = ConversationSummaryBufferMemory(return_messages = True,
                                            max_token_limit= max_token_limit,
                                            llm = llm)
    return memory
    


def load_memory_as_str(memory: BaseMemory) -> str:
    return str(memory.load_memory_variables({})['history'])

def read_configs_from_toml(path: str) -> dict:
    with open(path, 'r') as toml_file:
        data = toml.load(toml_file)
    return data

 
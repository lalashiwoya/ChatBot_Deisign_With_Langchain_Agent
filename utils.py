from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

def init():
    llm = ChatOpenAI(temperature=0, model_name = "gpt-3.5-turbo", streaming = True)
    memory = ConversationBufferMemory(return_messages = True)
    return llm, memory
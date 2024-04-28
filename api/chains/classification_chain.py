from api.prompts import classification_chain_prompt
from operator import itemgetter
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

template = classification_chain_prompt.template

def create_classification_chain(llm):
    chain = (
        {"question": itemgetter("question"),
         "memory": itemgetter("memory")} |
        ChatPromptTemplate.from_template(template) |
        llm |
        StrOutputParser()
    )
    return chain
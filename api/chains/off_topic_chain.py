from api.prompts import off_topic_prompt
from operator import itemgetter
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

template = off_topic_prompt.template

def create_off_topic_chain(llm):
    chain = (
        {"question": itemgetter("question")} |
        ChatPromptTemplate.from_template(template) |
        llm |
        StrOutputParser()
    )
    return chain
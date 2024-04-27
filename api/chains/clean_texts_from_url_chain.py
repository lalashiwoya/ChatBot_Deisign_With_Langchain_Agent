from llama_index.core.node_parser import SentenceSplitter
from api.prompts import clean_texts_from_url_prompt
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from operator import itemgetter

template = clean_texts_from_url_prompt.template

def create_clean_texts_from_url_chain(llm):
    chain = (
    {"question": itemgetter("question")} | 
    ChatPromptTemplate.from_template(template) |
    llm |
    StrOutputParser()
)
    return chain
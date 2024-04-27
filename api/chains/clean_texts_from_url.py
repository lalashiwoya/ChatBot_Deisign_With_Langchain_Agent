from llama_index.core.node_parser import SentenceSplitter
from api.prompts import clean_texts_from_url
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from operator import itemgetter

template = clean_texts_from_url.template

def clean_texts_from_url_chain(llm):
    clean_text_chain = (
    {"question": itemgetter("question")} | 
    ChatPromptTemplate.from_template(template) |
    llm |
    StrOutputParser()
)
    return clean_text_chain
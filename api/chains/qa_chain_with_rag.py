from api.prompts.qa_prompt_with_rag import template
from service.llama_index_retrive import LlamaRetriever
from service.data_collect import WebPagesToDocuments
from operator import itemgetter
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from llama_index.embeddings.openai import OpenAIEmbedding
from api.utils import get_retriever


retriever = get_retriever(path = "config.toml")
def create_llm_finetun_chain(llm):
    chain = (
        {"question": itemgetter("question"),
        "context": retriever,
        "memory": itemgetter("memory")} |
        ChatPromptTemplate.from_template(template) |
        llm |
        StrOutputParser()
    )
    return chain



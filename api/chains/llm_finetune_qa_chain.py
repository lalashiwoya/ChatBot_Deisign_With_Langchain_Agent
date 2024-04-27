from api.prompts.qa_prompt_with_rag import template
from service.llama_index_retrive import LlamaRetriever
from service.data_collect import WebPagesToDocuments
from operator import itemgetter
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from llama_index.embeddings.openai import OpenAIEmbedding

path = "data/llm_finetune/urls/urls.txt"
if_clean_texts = False

docs = WebPagesToDocuments(path = path, clean_texts=if_clean_texts).docs

retriever = LlamaRetriever(db_path="data/llm_finetune/db",
                           embeddings_model=OpenAIEmbedding(model="text-embedding-3-small"),
                           docs = docs)


def create_llm_finetun_chain(llm):
    chain = (
        {"question": itemgetter("question"),
        "context": retriever} |
        ChatPromptTemplate.from_template(template) |
        llm |
        StrOutputParser()
    )
    return chain



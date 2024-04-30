from api.prompts.qa_prompt_with_rag import template
from service.data_collect import WebPagesToDocuments
from operator import itemgetter
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from llama_index.embeddings.openai import OpenAIEmbedding
from api.utils import get_router_retriever
from langchain_core.runnables import RunnableLambda

retriever = get_router_retriever(path = "config.toml")



def create_llm_finetun_chain(llm):
    chain = (
        {"question": itemgetter("question"),
        "context": itemgetter("question")| RunnableLambda(retriever.get_relevant_documents),
        "model_name": lambda x: x["user_settings"].llm_model_name,
        "memory": itemgetter("memory")} |
        ChatPromptTemplate.from_template(template) |
        llm |
        StrOutputParser()
    )
    return chain



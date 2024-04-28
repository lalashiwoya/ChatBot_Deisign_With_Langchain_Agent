from service.data_collect import WebPagesToDocuments, PdfPagesToDocuments, YoutubePagesToDocuments
from llama_index.embeddings.openai import OpenAIEmbedding
from service.llama_index_retrive import LlamaRetriever
from utils import read_configs_from_toml

def get_retriever(path: str) -> LlamaRetriever:

    configs = read_configs_from_toml(path)

    # path = "data/llm_finetune/urls/urls.txt"
    # if_clean_texts = False

    web_docs = WebPagesToDocuments(path = configs["dataset"]["llm_finetune"]["url_path"], 
                            clean_texts=configs["dataset"]["llm_finetune"]["if_clean_texts"]).docs
    pdf_docs = PdfPagesToDocuments(path = configs["dataset"]["llm_finetune"]["pdf_dir"],
                                   clean_texts=configs["dataset"]["llm_finetune"]["if_clean_texts"]).docs
    youtube_docs = YoutubePagesToDocuments(path = configs["dataset"]["llm_finetune"]["youtube_urls"], 
                                           clean_texts=configs["dataset"]["llm_finetune"]["if_clean_texts"]).docs
    docs = web_docs + pdf_docs + youtube_docs
    

    retriever = LlamaRetriever(db_path=configs["dataset"]["llm_finetune"]["db_path"],
                            chunk_size = configs["llama_index"]["chunk_size"],
                            embeddings_model=OpenAIEmbedding(model="text-embedding-3-small"),
                            docs = docs)
    return retriever
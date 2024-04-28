from typing import List
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from llama_index.core.schema import Document
from langchain_core.retrievers import BaseRetriever
from llama_index.core.embeddings import BaseEmbedding
from langchain.chat_models.base import  BaseChatModel
from llama_index.core import Settings
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex
import os
from langchain.chat_models import ChatOpenAI
from utils import init_llm

class LlamaRetriever(BaseRetriever):
    embeddings_model: BaseEmbedding
    db_path: str
    docs: List[Document]
    top_k: int=3
    is_stored: bool = False
    chunk_size: int=1024
    
    
    
    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> str:
        retriever = self.get_retriever()
        response = retriever.query(query['question'])
        final_output = ""
        for i, node in enumerate(response.source_nodes):
            url = node.metadata['doc_id']
            text = node.text
            url_with_text = f"Source: {i+1}, URL: {url}, \n\n Text: {text}"
            final_output += url_with_text + "\n"
        return final_output
        
    
    def get_retriever(self):
        
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            
            Settings.llm = init_llm()
            Settings.embed_model = self.embeddings_model
            Settings.chunk_size = self.chunk_size
            Settings.chunk_overlap = 30
            
            index = VectorStoreIndex.from_documents(self.docs)
            index.storage_context.persist(persist_dir=self.db_path)
            
        else:
            storage_context = StorageContext.from_defaults(persist_dir=self.db_path)
            index = load_index_from_storage(storage_context)
            
        retriever = index.as_query_engine(similarity_top_k=self.top_k)
        
        return retriever
    
    
    
     
    
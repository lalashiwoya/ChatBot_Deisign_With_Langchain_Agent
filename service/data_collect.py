from api.chains.clean_texts_from_url import clean_texts_from_url_chain
from langchain_core.runnables.base import RunnableSequence
from typing import List
from langchain.chat_models.base import  BaseChatModel
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter


class DocumentRefiner:
    def __init__(self, llm: BaseChatModel,
                 chunk_size:int = 3000, 
                 chunk_overlap:int = 0):
        self.chain = clean_texts_from_url_chain(llm)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_sentence_splitter(self):
        return SentenceSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def refine_html_files(self, docs: List[Document]) -> List[Document]:
        cleaned_docs = []
        splitter = self.get_sentence_splitter()
        for doc in docs:
            cleaned_doc_segments = ""
            doc_segments = splitter.get_nodes_from_documents([doc])

            for seg in doc_segments:
                try:
                    response = self.chain.invoke({"question": seg.text})
                    cleaned_doc_segments += response.text + "\n"
                except Exception as e:
                    print(f"Error processing segment: {e}")

            doc.text = cleaned_doc_segments
            cleaned_docs.append(doc)

        return cleaned_docs


from api.utils import get_router_retriever
from langchain.agents import Tool

def create_retriever_as_tool(tool_configs: dict, general_configs: dict):
    # retriever = get_router_retriever(path = config_path)
    tool_name = tool_configs["qa_retriever"]["name"]
    tool_description = tool_configs["qa_retriever"]["description"]
    retriever = get_router_retriever(configs=general_configs)
    qa_retriever = Tool.from_function(name=tool_name,
                                        func=retriever.get_relevant_documents,
                                        description= tool_description
                                        )
    return qa_retriever
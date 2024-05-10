from api.tools.retriever import create_retriever_as_tool
from api.tools.off_topic_tool import create_off_topic_tool

def init_tools(tool_configs: dict, configs: dict):
    retriever = create_retriever_as_tool(tool_configs, configs)
    off_topic_tool = create_off_topic_tool(tool_configs=tool_configs)

    tools = [off_topic_tool, retriever]
    return tools
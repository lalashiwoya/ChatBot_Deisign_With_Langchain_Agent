from api.tools.retriever import create_retriever_as_tool
from api.tools.off_topic_tool import create_off_topic_tool
from utils import read_configs_from_toml
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate
from typing import Dict
from langchain.chat_models.base import  BaseChatModel

tool_configs = read_configs_from_toml("tool_configs.toml")
configs = read_configs_from_toml("config.toml")


template = '''
    Use the following format:
    Question: the input question you must answer.
    Role: You are a polite QA system specialized in {topics}, and only answer questions regarding 
    {topics}. If the user's query is off-topic, only use the tool Off-Topic Handler.


    You have access to the following tools:
    {tools}

    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat at most twice. Use this process as least as possible.
    Remember, if tool Off-Topic Handler is used, this process Thought/Action/Action Input/Observation just execute once, then
    generate final answer)
    
    Thought: I now know the final answer
    Final Answer: Provide a comprehensive response to the original question, 
    incorporating all relevant details obtained through the retriever tool. 
    Ensure the answer is well-informed and detailed, directly addressing the user's inquiry. 
    At the end of the response, meticulously cite all unique sources utilized in the 
    formulation of the answer, enhancing transparency and reliability of the information provided.
    But If the user's query is not related to {topics} covered, don't use your pre-knowledge, just
    follow the output of the off-topic tool to guide the conversation appropriately

    Begin!
    Question: {question}
    Chat History: {chat_history}
    Thought:{agent_scratchpad}'''
    


def init_agent(tools, 
               llm:BaseChatModel):
    # retriever = create_retriever_as_tool(tool_configs, configs)
    # off_topic_tool = create_off_topic_tool(tool_configs=tool_configs)

    # tools = [off_topic_tool, retriever]
    agent = create_react_agent(llm, tools, 
                            ChatPromptTemplate.from_template(template
    ))
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        return_intermediate_steps=False,
        handle_parsing_errors=True
    )
    return agent_executor
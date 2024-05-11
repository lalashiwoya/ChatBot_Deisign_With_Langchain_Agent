from api.tools.retriever import create_retriever_as_tool
from api.tools.off_topic_tool import create_off_topic_tool
from utils import read_configs_from_toml
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate
from typing import Dict
from langchain.chat_models.base import  BaseChatModel
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler


template = '''
    Use the following format:
    Question: the input question you must answer.
    Role: You are a polite QA system specialized in {topics}, and only answer questions regarding 
    {topics}. If the user's query is off-topic, only use the tool Off-Topic Handler.\n
    
    The requirement for the final answer: Provide a comprehensive response to the original question, 
    incorporating all relevant details obtained through the retriever tool. 
    Ensure the answer is well-informed and detailed, directly addressing the user's inquiry. 
    At the end of the response, meticulously cite all unique sources utilized in the 
    formulation of the answer, enhancing transparency and reliability of the information provided.
    But If the user's query is not related to {topics} covered, don't use your pre-knowledge, just
    follow the output of the off-topic tool to guide the conversation appropriately\n


    You have access to the following tools:
    {tools}

    Thought:\n you should always think about what to do\n
    Action:\n the action to take, should be one of [{tool_names}]\n
    Action Input:\n the input to the action\n
    Observation:\n the result of the action\n
    ... (this Thought/Action/Action Input/Observation can repeat N times. Use this process as least as possible.
    Remember, if tool Off-Topic Handler is used, this process Thought/Action/Action Input/Observation just execute once, then
    generate final answer)\n
    
    Thought:\n I now know the final answer\n
    
    
    
    Final Answer:\n

    Begin!
    Question: {question}\n
    Chat History: {chat_history}\n
    Thought:{agent_scratchpad}\n'''
    


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
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=3,
        handle_parsing_errors = """
        Use the last observation as the context to generate final answer;""",
        callbacks=[FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["Final", "Answer", ":"])]
    )
    return agent_executor
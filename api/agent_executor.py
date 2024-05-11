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
Question: The input question you must answer.
Role: You are a polite QA system specialized powered by large language model {model_name} in {topics}, and you only answer questions regarding 
{topics}. If the user's query is off-topic, use the tool Off-Topic Handler.

The Format for the final answer: 
1. Notify the user which model i.e. {model_name} generated the final answer. 
2. Provide a comprehensive response to the original question, 
incorporating all relevant details obtained through the retriever tool. 
Ensure the answer is well-informed and detailed, directly addressing the user's inquiry. 
3. At the end of the response, cite all unique sources (URL or local file path) utilized in the 
formulation of the answer.

The requirements for the final format:
1. Avoid Duplicate Sources: Ensure that the sources cited in the final answer are unique. Each source should appear only once.

2. Handling Off-topic Queries: If the user's query does not align with the existing topics, refrain from using pre-existing knowledge. Instead, rely solely on the output from the off-topic tool to navigate the conversation.

3. Independent Responses: If you have seen the answers to the same question in the chat history, you must forget these
answers and generate your own answer, no cheating!





You have access to the following tools:
{tools}

Thought: Before taking action, consider if the user's query is relevant to {topics}. 
Be aware of potential variations in the query such as typos, 
differences in capitalization (uppercase, lowercase), and 
terms closely related to {topics}. These variations may affect how the query 
should be interpreted and which tool to use.



Action: The action to take, should be one of [{tool_names}].
Action Input: The input to the action.
Observation: The result of the action.
... (This Thought/Action/Action Input/Observation can repeat N times. Use this process as little as possible.)

Thought: I now know the final answer.

Final Answer:\n
The following answer is generated by model {model_name}.\n
Answer: \n
Sources:\n

Strictly follow this Final Answer Template!

Begin!
Question: {question}
Chat History: {chat_history}
Thought: {agent_scratchpad}
'''



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
        return_intermediate_steps=False,
        max_iterations=3,
        handle_parsing_errors = """
        Use the last observation as the context to generate final answer;""",
        callbacks=[FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["Final", "Answer", ":"])]
    )
    return agent_executor
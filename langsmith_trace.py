from dotenv import load_dotenv
load_dotenv(".env")

import argparse
from utils import read_configs_from_toml, init_memory, init_llm
from langsmith_evaluation.langsmith_dataset import create_langsmith_dataset
from langsmith import Client
from langsmith_evaluation.langsmith_dataset import create_sample_topics, create_sample_user_settings
from langsmith.schemas import Run, Example
from llama_index.core.evaluation import CorrectnessEvaluator
import nest_asyncio
import asyncio
nest_asyncio.apply()
from llama_index.llms.openai import OpenAI
from langsmith.evaluation import aevaluate
from api.tools.tool_list import init_tools
from api.agent_executor import init_agent


# config_path = "langsmith_evaluation/config.toml"
# configs = read_configs_from_toml(config_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Langsmith Settings")
    parser.add_argument("--langsmith_config_path", type = str, default="langsmith_evaluation/config.toml")
    parser.add_argument("--config_path", type = str, default="config.toml")
    parser.add_argument("--tool_config_path", type = str, default="tool_configs.toml")
    parser.add_argument("--dataset_name", type = str, help = """Name of the current 
                        Langsmith dataset. The dataset will only be created if this 
                        name has not been used to create a dataset before.""")
    parser.add_argument("--dataset_description", type = str, help = "Description of your langsmith dataset", default="Test sample dataset")
    parser.add_argument("--experiment_prefix", type = str, help = "Prefix of your current experiment", default="correctness")
    args = parser.parse_args()
    configs = read_configs_from_toml(args.config_path)
    langsmith_configs = read_configs_from_toml(args.langsmith_config_path)
    tool_configs = read_configs_from_toml(args.tool_config_path)
    
    client = Client()

    
    
    create_langsmith_dataset(client=client, dataset_name=args.dataset_name, 
                             dataset_description=args.dataset_description,
                             csv_path=langsmith_configs["langsmith"]["question_answer_csv_file_path"])
    
    llm = init_llm(model_name=langsmith_configs["agent"]["model_name"])
    tools = init_tools(tool_configs=tool_configs,
                       configs=configs)
    memory = init_memory(llm)
    agent = init_agent(llm=llm,
                       tools=tools)
    
    
    async def get_chatbot_response(dataset_input: dict):
        question = dataset_input['question']
        chat_history = dataset_input['chat_history']
        
        
        for i in range(len(chat_history)):
            memory.save_context({"input": chat_history[i]['input']}, {"output": chat_history[i]['output']})
        topics = create_sample_topics()
        user_settings = create_sample_user_settings(langsmith_configs)
        agent_input = {"question": question,
                                    "chat_history": memory,
                                    "topics": topics,
                                    "model_name": user_settings.llm_model_name}
        response_content = []
        async for chunk in agent.astream(agent_input):
                content = chunk['messages'][0].content
                marker = "Final Answer:"
                if marker in content:
                    response = content.split(marker)[-1].strip()

                    response_content.append(response)
        return " ".join(response_content)
    
    def correctness(run: Run, example: Example) -> dict:
        correctness_evaluator = CorrectnessEvaluator(OpenAI(langsmith_configs["evaluator"]["model_name"]))
        result = asyncio.run(correctness_evaluator.aevaluate(
            query=example.inputs.get("question"),
            response=run.outputs.get("output"),
            reference=example.outputs.get("reference")
        ))

        return {
            "key":"correctness",
            "score":result.score/5,
            "comment":result.feedback
        }
    
    experiment_results = asyncio.run(aevaluate(
        get_chatbot_response, 
        data=args.dataset_name,  
        # evaluators=[correctness],  
        evaluators=[correctness],
        experiment_prefix=args.experiment_prefix,  
        metadata={
        "version": "1.0.0",
        },
    ))
    
 

    
    
    
    
    


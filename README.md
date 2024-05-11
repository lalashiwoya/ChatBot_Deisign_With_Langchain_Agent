# Chatbot Project (Langchain Agent Implementation)
My initial version of the chatbot was implemented using a router chain, where I can define the sequence of actions in a hardcoded way. However, issues arose with this approach:
- The router chain includes a classification chain to determine if a user's query is off-topic.
- If a user's previous query was "What is LLM fine-tuning?" and the next question is "Why is it important?", the latter might be classified as off-topic despite memory being fed to the classification chain.

The agent leverages the reasoning capabilities of LLMs, allowing it to decompose tasks into smaller subtasks and determine the order of actions and identifie the most appropriate tools for each specific action. Memory plays a more crucial role here. I switched from using `initialize_agent`, which is more common in tutorials but now deprecated, to `create_react_agent` for creating an agent.

Despite its advantages, the agent implementation has its drawbacks:
- Due to the dependency on the LLM's reasoning capabilities, the thinking process may not finish in time or within the iteration limit, resulting in no answer being returned. Unlike the agent-based approach, the router chain design consistently returns an answer, although it may not always be accurate or relevant.

- There is essentially a single, comprehensive prompt that governs the behavior of the Large Language Model (LLM). This prompt includes e.g, final answer formatting, final answer requirement, tool usage suggestions and more. Adhering to these complex requirements poses significant challenges, particularly for GPT-3.5. For example, despite explicit demands for source uniqueness in the final answers, GPT-3.5 sometimes fails to comply. Additionally, there are occasions where it does not adhere to the requested answer format, highlighting the limitations in its ability to retain sets of instructions compared to its successor, GPT-4.


While the upgrade from GPT-3.5 to GPT-4 offers minimal improvements in a router chain setup, it is significantly more effective in an agent-based implementation.


For the next phase, I plan to implement LangGraph to apply control flow constraints on the Large Language Model (LLM). 



## Environment Setup
1. **Create and activate a Conda environment**:
    ```bash
    conda create -y -n chatbot python=3.11
    conda activate chatbot
    ```
2. **Install required packages**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up environment variables**:
    - Write your `OPENAI_API_KEY` in the `.env` file. A template can be found in `.env.example`. 
    ```bash
    source .env
    ```
## Running the Application
To start the application, use the following command:

```bash
chainlit run app.py
```

## Features

### User Setting Panel
Users have the option to select the specific LLM (language learning model) they prefer for generating responses. The switch between different LLMs can be accomplished within a single conversation session.

<img src="images/setting_panel.png" alt="Setting Panel" width="50%">


### QA with RAG
- **Various Information Source**: The chatbot can retrieve information from web pages, YouTube videos, and PDFs.
- **Source Display**: You can view the source of the information at the end of each answer.
- **LLM Model Identification**:  The specific LLM model utilized for generating the current response is indicated.
- **Router retriever**: Easy to adapt to different domains, as each domain can be equipped with a different retriever.

### Conversation Memory
- **Memory Management**: The chatbot is equipped with a conversation memory feature. If the memory exceeds 500 tokens, it is automatically summarized.

### Langsmith Evaluation

To evaluate model generation against human references or log outputs for specific test queries, use Langsmith.

1. Register an account at [Langsmith](https://smith.langchain.com/).
2. Add your `LANGCHAIN_API_KEY` to the `.env` file.
3. Execute the script with your dataset name: 
   ```bash
   python langsmith_tract.py --dataset_name <YOUR DATASET NAME>
   ```
4. Modify the data path in `langsmith_evaluation/config.toml` if necessary (e.g., path to a CSV file with question and answer pairs).
<img src="images/langsmith-correctness.png" alt="Langsmith" width="50%">

### Recording Human Feedback with Literal AI
Use Literal AI to record human feedback for each generated answer. Follow these steps:

1. Register an account at [Literal AI](https://cloud.getliteral.ai/).
2. Add your `LITERAL_API_KEY` to the `.env` file.
3. Once the `LITERAL_API_KEY` is added to your environment, run the command `chainlit run app.py`. You will see three new icons as shown in the image below, where you can leave feedback on the generated answers.

<img src="images/literal_ai_web.png" alt="Literal_AI_Web" width="50%">

4. Track this human feedback in your Literal AI account. You can also view the prompts or intermediate steps used to generate these answers.

<img src="images/literal_ai_backend.png" alt="Literal_AI_Web" width="50%">

### User Authentication and User Past Chat Setup

This guide details the steps for setting up user authentication in your application. Each authenticated user will have the ability to view their own past interactions with the chatbot.

1. Add your APP_LOGIN_USERNAME and APP_LOGIN_PASSWORD to the `.env` file.
2. Run the following command to create a secret which is essential for securing user sessions:
   ```bash
   chainlit create-secret
   ```
   Copy the outputted CHAINLIT_AUTH_SECRET and add it to your .env file
3. Once you launch your application, you will see a login authentication page
4. Login with your APP_LOGIN_USERNAME and APP_LOGIN_PASSWORD
5. Upon successful login, each user will be directed to a page displaying their personal chat history with the chatbot.

![Web Page](images/user_auth_past_chat.gif)


## Presentation

Below is a preview of the web interface for the chatbot:

![Web Page](images/present_web.gif)

## Configuration

To customize the chatbot according to your needs, define your configurations in the `config.toml` file and `tool_configs.toml` where you can define the name and descriptions of your tools.



template = """

topics: 
    - Large Language Models (LLM) finetuning, 
    - explainable ai

As a QA system equipped to handle user interactions related to 
topics, your task is to evaluate and 
categorize user inquiries. With the context provided by the chat history, 
classify each question as 'General QA' if it directly relates to any of the topics. 

If the question is not about any of the topics, 
classify it as 'Other'.

Utilize the chat history "{memory}" to better understand the context of 

the current question, as it may contain key information that determines 

whether "it," "this," or "that" in the user's query is referencing any of the topics.

Please review the user's question and assign the appropriate category:

Current Question: "{question}"

Classification:


"""
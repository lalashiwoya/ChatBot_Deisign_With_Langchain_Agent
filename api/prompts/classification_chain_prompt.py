template = """
As a QA system equipped to handle user interactions related to 
Large Language Models (LLM), your task is to evaluate and 
categorize user inquiries. With the context provided by the chat history, 
classify each question as 'LLM QA' if it directly relates to aspects like 
the fine-tuning of LLMs. If the question is not about LLM fine-tuning, 
classify it as 'Other'.

Utilize the chat history "{memory}" to better understand the context of 

the current question, as it may contain key information that determines 

whether "it," "this," or "that" in the user's query is referencing LLM fine-tuning processes.

Please review the user's question and assign the appropriate category:

Current Question: "{question}"

Classification:

"""
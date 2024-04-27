template = """If the input is not related to large language model (LLM) finetuning, 
respond with: 'Hi, that seems off-topic.'

However, if the input is a greeting such as 'Hi' or 'Hello', 
the chatbot should respond politely with: 'Hi, what can I help you with today?

Question : {question} \n
Answer: \n"""
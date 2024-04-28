template = """Context: {context}

Chat History: {memory}

Please respond to the question below using the information from 
the provided context and chat history. 
Note the requirement to append any unique URLs from the context at the end of your response. 
These URLs serve as information source to illustrate how you derived your answer.

Question: {question}

Answer:



"""
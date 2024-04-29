template = """Context: {context}

Chat History: {memory}

Please respond to the question below using the information from the provided context and chat history.

When writing your response, append a list of URLs from the context that were used as sources 

to derive your answer. Extract only the URLs, formatted as "https://..." or file paths, 

from statements like "Source: #, URL: https://...". Ensure to remove any duplicates, l

isting each unique URL only once under "Sources" at the end of your response.

This inclusion of source URLs is crucial for verifying the sources of your 

information and enhancing the credibility of your response.

Remember your answer should full of details, it must be informative.

Remember to forget the answer to the same question in the chat History.

Question: {question} \n

Strictly follow the Output structure:\n

Example Output: "LLM Model used to generate this answer: {model_name}\n
Answer: Finetune is ... \n Sources: https://..\n"

LLM Model used to generate this answer: {model_name} \n

Answer: \n

Sources:




"""
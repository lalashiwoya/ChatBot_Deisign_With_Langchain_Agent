template = """
Question: {question} \n

Context: {context}

Chat History: {memory}

LLM Model Name: {model_name}

If you see the answers to the current question by different LLM Models in the chat History, 

you have to forget these answers from your memory, otherwise it's cheating!

Please respond to the question below using the information from the provided "Context" and "Chat History".

When writing your response, append a list of URLs or file path from the "Context" that were used as sources 

to derive your answer. Ensure to remove any duplicates, listing each unique URL or file path only once under "Sources" at the end of your response.

This inclusion of source URLs is crucial for verifying the sources of your 

information and enhancing the credibility of your response.

Remember your answer should full of details, it must be informative.







Strictly follow the Output structure:\n

Example Output: "LLM Model used to generate this answer: {model_name}\n Answer: xxx \n Sources: xxx\n"

LLM Model used to generate this answer: {model_name} \n

Answer: \n

Sources:




"""
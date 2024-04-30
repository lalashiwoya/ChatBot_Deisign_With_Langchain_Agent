

template = """

topics: {topics}

Question: "{question}"

As a QA system focused on specified topics, your task is to evaluate and categorize each user inquiry. 

Utilize the chat history provided in "{memory}" to determine the relevance of the question . 
This context is crucial, especially if the question uses pronouns like "it," "this," or "that," 
which may refer to a topic from the memory.

Classify the question as:
- 'General QA' if it directly relates to the topics.
- 'Other' if it does not pertain to the topics.

Pay special attention to grammatical variations and similar phrases of the topics discussed

Only the classifications 'General QA' or 'Other' are permitted. No other answer should be used.


Answer:\n

"""
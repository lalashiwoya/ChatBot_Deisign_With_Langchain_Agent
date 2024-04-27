template = """You are a system designed to clean and preprocess text. The text will be used for 
information retrieval, so it's essential to remove any URLs, HTML tags, and Markdown 
formatting. Keep the urls if they contain github or huggingface. Ensure that the text is clean, readable, and free of any unnecessary elements. 
Be creative and thorough in your approach to text cleaning.
Question : {question} \n
Answer: \n
"""
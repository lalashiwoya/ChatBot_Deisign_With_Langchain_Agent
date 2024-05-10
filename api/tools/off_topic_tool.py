from langchain.agents import Tool

def foo(query: str):
    return f"""If a user greets the chatbot with phrases such as 'Hi,' 'Hello,' or 
    similar, the tool will ensure a warm and appropriate response is returned. 
    If the user's message deviates from relevant topics, the tool offers a polite 
    reminder of its capabilities while maintaining a friendly and welcoming tone. 
    This approach helps keep the conversation focused and engaging, ensuring the user 
    feels supported and guided toward productive interactions. """

def create_off_topic_tool(tool_configs: dict):
    off_topic_tool = Tool.from_function(
            name=tool_configs['off-topic']['name'],
            description=tool_configs['off-topic']['description'],
            func=foo
    )
    return off_topic_tool
from chainlit.input_widget import Select, Switch, Slider, TextInput
import chainlit as cl
from api.pydantic_model import UserSettings
from utils import init_llm
from api.agent_executor import init_agent

def init_settings():
    settings = [
        Select(
            id="llm_model_name",
            label="Model Selection",
            values=["gpt-3.5-turbo", "gpt-4"],
            initial_index=0,
        )
        
        
    ]
    return settings

def set_user_settings_as_pydantic_model(settings):
    try:
        user_settings = UserSettings(
            llm_model_name = settings['llm_model_name']
        )
        return user_settings
    except ValueError:
        print("Invalid User Settings")
        
@cl.on_settings_update
def update_user_session(settings, tool_configs, configs):
    user_settings = set_user_settings_as_pydantic_model(settings)
    llm = init_llm(user_settings.llm_model_name)
    agent = init_agent(tool_configs=tool_configs,
                       configs=configs,
                       llm=llm)
    if user_settings is not None:
        print("="*20)
        print(user_settings)
        cl.user_session.set("user_settings", user_settings)
        cl.user_session.set("agent", agent)
        


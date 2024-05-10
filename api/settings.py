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
def update_user_session(settings):
    user_settings = set_user_settings_as_pydantic_model(settings)
    # llm = init_llm(user_settings.llm_model_name)
    # print(cl.user_session.get("tools"))
    # agent = init_agent(
    #                    llm=llm,
    #                    tools=cl.user_session.get("tools"))
    
    if user_settings != cl.user_session.get("user_setting"):
        print("="*20)
        print(user_settings)
        cl.user_session.set("user_settings", user_settings)
        # cl.user_session.set("agent", agent)
        


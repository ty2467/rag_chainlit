'''
    Imports for loading OPENAI_API_KEY
'''
import os
from dotenv import load_dotenv# find_dotenv


'''
    imports for agent using tools
'''
import g_a
import lc_rag
import llm_tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

'''
    Import for user interface
'''
import chainlit as cl

'''
    Imports for llm
'''
from langchain_community.chat_models import ChatOpenAI


'''
   Load in OPENAI_API_KEY
'''
dotenv_path = os.path.join(os.path.expanduser('~'), '.env')
_ = load_dotenv(dotenv_path) # read local .env file

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

'''
    Defining Model
'''
llm_model = "gpt-3.5-turbo"



@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(temperature=0, model=llm_model, openai_api_key=OPENAI_API_KEY, streaming=True)
    tools = [g_a.search, llm_tool.chat, lc_rag.rag]
    agent= initialize_agent(
        tools,
        model, 
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose = True)
    cl.user_session.set("agent", agent)


@cl.on_message
async def query_llm(message: cl.Message):
    agent= cl.user_session.get('agent')
    
    response = await agent.acall(message.content, 
                                     callbacks=[
                                         cl.AsyncLangchainCallbackHandler()])
    print(response)
    await cl.Message(response["output"]).send()
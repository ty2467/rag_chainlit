#Chatbot using openai
'''
imports for loading in OPENAI_API_KEY
'''
import os
from dotenv import load_dotenv# find_dotenv

'''
imports for openai, to setup and call openAI() client
'''
import openai

'''
langchain libraries for settingup tool
'''
from langchain.agents import tool

"""
    Set up OPENAI_API_KEY
"""

dotenv_path = os.path.join(os.path.expanduser('~'), '.env')
_ = load_dotenv(dotenv_path) # read local .env file

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY 


'''
    openai client
'''
client = openai.OpenAI() #client object

'''
    Initializing context, bot memory
'''

context = [
    {'role': 'system', 
     'content': """you are a chatbot who will provide answers
     to simple questions from another llm """}
]

"""
    Calls model, gets a passed in context
"""
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )

    return (response.choices[0].message.content)


'''
    Call model and appends, extends, context
'''
def collect_messages(prompt): 
    #appends the new user prompt
    context.append({'role':'user', 'content':f"{prompt}"}) 
    response = get_completion_from_messages(context) 
    #appends the response from llm
    context.append({'role':'assistant', 'content':f"{response}"}) 
    return response



"""
    The tool to do the chatting feature Essentially, agent has an llm in 
    itself, which interacts with a different llm that is a 
    chatbot that has memory
"""

@tool
def chat(query: str):
    """
    Uses base llm without any other tools to answer simple\
    questions. Do not answer the question yourself, but pass the \
    user's prompt, denoted by the variable (here in between backticks)\
    `query` to the collect_messages function, and pass out the returned\
    response from that function which will call another llm\
    For example: 'what is the color of the sky on a clear day'\
    user this only for answers and responses that you\
    are extremely confident about.  """
    gpt_response = collect_messages(query)
    return gpt_response
    
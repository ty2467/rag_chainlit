'''
    Imports for llm, and setting up tool
'''
from langchain.agents import tool
from langchain_openai import ChatOpenAI

'''
    Import for google api
'''
from googleapiclient.discovery import build

'''
    Imports for setting up OPENAI_API_KEY
'''
import os
from dotenv import load_dotenv

'''
    OPENAI_API_KEY setup 
'''
dotenv_path = os.path.join(os.path.expanduser('~'), '.env')
_ = load_dotenv(dotenv_path) # read local .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

'''
    top n search result 'macro' setup
'''
TOP_N_THREASHHOLD = 4


'''
    Google custom search setup
'''
API_KEY = 'AIzaSyDyGt9uhHkqyeSjFs3mvqzP8fAEQ1MZpY4'
CSE_ID = 'b626bf8b5fd13438d'

'''
    LLM model set up
'''
llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0, model=llm_model, openai_api_key=OPENAI_API_KEY)


'''
    function that does the search query
'''
def google_search(query, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res

'''
    function that obtains the top n 
'''
def top_n_search_results(query):
    temp_res = google_search(query, API_KEY, CSE_ID)
    keys = temp_res.keys()
    keys_included = list(keys)[:-1]
    no_items = {key: temp_res[key] for key in keys_included} 
    items = temp_res['items']
    top_n_items  = {"items": items[0:TOP_N_THREASHHOLD]}
    top_n_result = no_items | top_n_items
    return top_n_result


'''
    Google search tool
'''
@tool
def search(query: str):
    """Uses google api to search up documents and\
    results for queries from the user., use this for any \
    questions that local documents cannot provide context\
    for answering, or when the base llm cannot answer\
    with full confidence without looking up extra information \
    The input should always be a query string \
    and this function will return the query result from\
    google's api."""
    results = top_n_search_results(query)
    return results
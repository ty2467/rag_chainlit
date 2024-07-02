'''
    Imports for setting up db index (that can be queried), uses embeddings
'''
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import OpenAIEmbeddings


'''
    Imports for settingup openai api key
'''
import os
from dotenv import load_dotenv
'''
    imports for making this into a tool
'''
from langchain.agents import tool

'''
    Imports for openai replacement model
'''
from langchain_openai import OpenAI


'''
    OPENAI_API_KEY setup
'''

dotenv_path = os.path.join(os.path.expanduser('~'), '.env')
_ = load_dotenv(dotenv_path) # read local .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



'''
    Settingup embedding model
'''
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


'''
    Loading in corpus
'''
file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)


'''
    Setting up db index, embedding and indexing in one 'step'
'''
index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=embeddings,
).from_loaders([loader])


'''
So for the next steps, what we are to do is this:
1. Setup a persistent vector database
2. Do efficient rag on it.
Really, all these can be achieved through openai file-search

'''


'''
    Setting up tool that does rag. Demonstrates the ability to retreive data from corpus.
'''
@tool
def rag(query: str):
    """ uses rag technique to answer query question\
        in combination with files. 
        Use this only for questions that pertain to subjects\
        that you have access information to from local files that\
        you can load in. These subjects only contain topics delimited\
        within the triple backticks:\
        ```\
        out door clothing catalog\
        ```\
        The input should always be a query string, and\
        after getting an object from the index.query engine, you\
        should answer the question in a string with your results"""
    
    llm_replacement_model = OpenAI(temperature=0, model='gpt-3.5-turbo-instruct', openai_api_key=OPENAI_API_KEY)
    response = index.query(query,  llm = llm_replacement_model)
    return response

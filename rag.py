from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
import openai
import initialize_db
import os
from dotenv import load_dotenv# find_dotenv


"""
    Set up OPENAI_API_KEY 
"""
dotenv_path = os.path.join(os.path.expanduser('~'), '.env')
_ = load_dotenv(dotenv_path) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

'''
    setup openai client object
'''
client = openai.OpenAI() #client object


'''
set up thread.
'''
# Create a thread and attach the file to the message

'''
langchain libraries for settingup tool
'''
from langchain.agents import tool

@tool
def rag_with_openai_vec_db(query: str):
  """ uses rag technique to answer query question\
    in combination with files. \
    Use this only for questions that pertain to subjects\
    that you have access information to from local files that\
    you can load in. These subjects only contain topics delimited\
    within the triple backticks:\
    ```\
    openai_chatbot.py file\
    ```\
    The input should always be a query string, and\
    after getting an object from the index.query engine, you\
   should answer the question in a string with your results"""
    
  thread = client.beta.threads.create(
    messages=[
      {
        "role": "user",
        "content": query,
      }
    ],
    tool_resources={
      "file_search": {
        "vector_store_ids": [initialize_db.vector_store.id]
      }
    }
  )
  run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id, assistant_id=initialize_db.assistant.id
  )

  messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

  message_content = messages[0].content[0].text
  annotations = message_content.annotations
  citations = []
  for index, annotation in enumerate(annotations):
      message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
      if file_citation := getattr(annotation, "file_citation", None):
          cited_file = client.files.retrieve(file_citation.file_id)
          citations.append(f"[{index}] {cited_file.filename}")

  return message_content.value
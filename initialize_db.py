from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
import openai

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
    Setting up openai vector store
        Assistant:
            LLM that uses models tools  (it does seem to suggest
'''
assistant = client.beta.assistants.create(
    name = "Code reading assistant",
    model = "gpt-4o",
    tools = [{"type": "file_search"}]
)
#Create vector_store
vector_store = client.beta.vector_stores.create(name="Professional Python Code Reader")

# Read files: setup filepath and file_stream (stream to pass the data into)
file_paths = ["./openai_chatbot.py"]
file_streams = [open(path, "rb") for path in file_paths]

#upload and poll status
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, 
    files=file_streams
)

#update assistant
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
 
'''
obtains file ids
    later fed into thread
'''
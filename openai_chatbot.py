'''
DO NOT RUN THIS. THIS IS MEANT TO BE READ AS AN EXAMPLE FILE BY OPENAI'S ASSISTANT
'''
#Chatbot using openai
import sys
import os
import openai
from dotenv import load_dotenv# find_dotenv


"""
    Set up openAI()
"""
dotenv_path = os.path.join(os.path.expanduser('~'), '.env')
_ = load_dotenv(dotenv_path) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

'''
    Creates object
'''
client = openai.OpenAI() #client object


'''
    Creating context of a bot to give it memory
'''
context = [
    {'role': 'system', 'content': """you are a knowlegded professional about
     the world of soccer. you are to answer questions by the user about
     FIFA world cup histories, and you are to answer like an encyclopedia """}
]

"""
    Calls model using context, and returns the content of the response
"""
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )

    return (response.choices[0].message.content)



def collect_messages(prompt):
    # inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    return response


def main(args):
    if len(args) != 2:
        print("Usage: python script_name.py <input>")
        sys.exit(1)

    input_arg = args[1]

    print(f'You entered: {input_arg}')

    while True:
        user_input = input("Enter new input (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting...")
            break
        gpt_response = collect_messages(user_input)
        print("printing here")
        print(gpt_response)

    

if __name__ == "__main__":
    exit(-1)
    main(sys.argv)
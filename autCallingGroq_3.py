

     # Chain of Thought


import os # The reason to import this is to access environment variables, such as the GEMINI_API_KEY, which is stored in the .env file.
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import json


# Directly take from grok python sdk (https://console.groq.com/docs/quickstart)
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


system_prompt = """
    You are an ai expert in breaking down complex problems asked by the user.
    On every user input you divide the problem into multiple steps:
    Step 1: Analyze: Analyze the problem, what the user is asking for
    Step 2: Think: Think how to find the solution of the problem, what concept does it uses.
    Step 3: Think: Start solving the problem
    Step 4: More thinking may take place according to the difficulty of the problem
    Step 5: Output: Give the result to the user

    Example:
    Input: What is a black hole?
    Output: {{ "step": "Analyze", "content": "The user is asking about the black hole, It is a space related relation, I have to answer accordingly"}}
    Output: {{ "step": "Think", "content": "Black hole is the most dense physical body in the universe."}}
    Output: {{ "step": "Think", "content": "It is something from which even light cannot pass."}}
    Output: {{ "step": "Output", "content": "Black hole is the most dense physical body in the universe. It is something from which even light cannot pass."}}

    Output only one step at a time. Once you output one result/step then output the next one.
"""


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is a black hole & why is it black? Respond in json"} ### VERY VERY IMPORTANT: If you want response in json then you must include the word "json" in the user input. If you don't include it then the model will throw an error. This is because the model is not able to understand that you want the response in json format. So, always include the word "json" in the user input if you want the response in json format.
    ### You can also write this in the system_query. That would also work!!
]


maxCalls = 10 # Safety net that will stop the loop after 10 calls to the model. This is to prevent infinite loops in case the model does not return the expected output.

while True and maxCalls > 0:
    maxCalls -= 1 

        # Groq API call
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Great for reasoning & JSON
        messages=messages,
        temperature=0.5,
        max_completion_tokens=300,
        # 👇 This forces Groq to return raw JSON matching your system prompt rules!
        response_format={"type": "json_object"} 
    )
    print(chat_completion.choices[0].message.content) # This is the raw response from the model, which is a string. It is not yet parsed into a python object. The model will return a string that looks like a JSON object, but it is still a string. We need to parse it into a python object using json.loads().
    print ("\n--------------\n")

    parsed_resp = json.loads(chat_completion.choices[0].message.content) # Parsed response to a python object

    messages.append({"role": "assistant", "content": chat_completion.choices[0].message.content})
    if parsed_resp.get('step') == 'Output':
        break
    
print("\nThe answer is complete.\n\n")
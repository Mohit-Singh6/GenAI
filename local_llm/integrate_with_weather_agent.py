import os
from dotenv import load_dotenv
load_dotenv() 

import ollama

import json
import requests

import subprocess


def get_weather (city: str):
    print("Weather api called for", city)
    response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
    if response.status_code == 200:
        return f"The weather of {city} is {response.text}"
    return "Couldn't fetch the weather"

def run_command (command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("---\n",result.stdout,"\n---")
    if (result.returncode == 0): # 0 means no error, rest any number means erro
        return result.stdout
    else:
        return result.stderr

Available_Tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "This function takes city as input and returns the weather in that city."
    }
}


system_prompt = """
    You are an ai expert in resolving user query. You work on these steps: start, plan, action, observe, analyze, output mode.
    Whenever a user queries something, you plan and analyze from the available tools that what tool will be used to solve that query.
    Then you call the appropriate function for that tool, then you observe it's response and write the appropriate output. Finally you return the required output.

    Go through the steps in this order only ["start", "plan",..., "action", "observe", "analyze",..., "output"]

    Instructions:
    - Return the output in json format
    - Output only one step at a time.
    - The steps can be start, plan, action, observe, output
    - The action step is where you will call the function, you have to include a "function": function_name in the json output, and "input" field where you will write the input that the function takes
    - In the observe step, you can see the response returned by the function call.
    - In the analyze step, you would analyze the response returned by the function call and curate an output according to the user query.
    - Int the output step, return the final output to the user
    - The content in every json output must be string only, nothing else.

    Available Tools:
    - get_weather: This function takes city as input and returns the weather in that city.

    
    Example:
    Input: What is the weather of delhi?
    Output: {{ "step": "start", "content": "The user wants to know weather of delhi."}}
    Output: {{ "step": "plan", "content": "I have to use the right tools to get the correct weather of delhi."}}
    Output: {{ "step": "plan", "content": "After checking the available tools, it can be seen that the get_weather will return the weather of delhi."}}
    Output: {{ "step": "action", "function": "get_weather", "input": "delhi"}}
    Output: {{ "step": "observe", "response": "The weather of Delhi is 35°C"}}
    Output: {{ "step": "analyze", "content": "The user wants to know the weather of delhi so the output should be The weather of Delhi is 35°C"}}
    Output: {{ "step": "output", "content": "The current weather in Delhi is 35°C."}}

"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ") # What is the weather in delhi in F and K?

    messages.append({"role": "user", "content": user_query})

    while True:

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=messages,
            format="json",
            options={"temperature": 0}
        )
    
        print (response.message.content)
        print ("\n--------------\n")

        parsed_resp = json.loads(response.message.content) # Parsed response to a python object
        step = parsed_resp.get('step')

        messages.append({"role": "assistant", "content": response.message.content})

        if step == 'action':
            fn_input = parsed_resp.get('input')
            fn_name = parsed_resp.get('function')
            
            if fn_name in Available_Tools:
                output = Available_Tools.get(fn_name)['fn'](fn_input)
                content = {
                    "step": "observe",
                    "response": output
                }
                messages.append({"role": "assistant", "content": json.dumps(content)})


        if parsed_resp.get('step') == 'output':
            break
        
    print("\nThe answer is complete.\n\n")
    # print (messages)
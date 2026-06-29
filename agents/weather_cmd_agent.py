import os
from dotenv import load_dotenv
load_dotenv() 

import json
import requests

import subprocess

from groq import Groq

from groq import RateLimitError # If the rate limit hits for one model, for that it is to handle that problem, and we can use a different model in this case.

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Define your primary and backup models
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def get_weather (city: str):
    print("Weather api called for", city)
    response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
    if response.status_code == 200:
        return f"The weather of {city} is {response.text}"
    return "Couldn't fetch the weather"

def run_command (command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("\n",result.stdout,"\n")
    if (result.returncode == 0): # 0 means no error, rest any number means erro
        return result.stdout
    else:
        return result.stderr

Available_Tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "This function takes city as input and returns the weather in that city."
    },
    "run_command": {
        "fn": run_command,
        "description": "Runs command on the system by taking string of command as input"
    }
}


system_prompt = """
    You are an ai expert in resolving user query. You work on these steps: start, plan, action, observe, analyze, output mode.
    Whenever a user queries something, you plan and analyze from the available tools that what tool will be used to solve that query.
    Then you call the appropriate function for that tool, then you observe it's response and write the appropriate output. Finally you return the required output.

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
    - run_command: Runs command on the system by taking string of command as input 

    Important Note:
    - when using the run_command tool, and using it to create or update any text in a file, don't add extra quotes or single quotes, because then they are also added in the file.
    - Example: 
        WRONG:  don't write the input as "echo 'Hello' > motivate.md" - this is wrong!
        CORRECT: Write the input as "echo Hello > motivate.md"

    
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
    user_query = input("Enter query: ") # Create a new file named raju.txt in the current directory and write "Hello, RAJU!" in that file.

    messages.append({"role": "user", "content": user_query})

    while True:

        try:
            chat_completion = client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=250,
                # 👇 This forces Groq to return raw JSON matching your system prompt rules!
                response_format={"type": "json_object"} 
            )
        except:
            # 👇 AUTOMATIC FALLBACK: If 70B is maxed out, use Llama 4 Scout instantly
            print("\nPrimary model LIMTI REACHED! Changing to fallback model....\n")
            chat_completion = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=250,
                # 👇 This forces Groq to return raw JSON matching your system prompt rules!
                response_format={"type": "json_object"} 
            )
        
        print(chat_completion.choices[0].message.content)
        print ("\n--------------\n")

        parsed_resp = json.loads(chat_completion.choices[0].message.content) # Parsed response to a python object
        step = parsed_resp.get('step')

        messages.append({"role": "assistant", "content": chat_completion.choices[0].message.content})

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
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

def create_or_write_file(filepath: str, content: str):
    """Creates a new file or completely overwrites an existing one."""
    # Using 'w' (write) mode. It handles any special characters cleanly.
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f" Successfully created/overwrote: {filepath}")

def append_to_file(filepath: str, content: str):
    """Appends text to the end of an existing file without wiping it."""
    # Using 'a' (append) mode.
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content)
    print(f" Successfully updated: {filepath}")

def read_file(filepath: str) -> str:
    """Reads the contents of a file securely."""
    if not os.path.exists(filepath):
        return "Error: File does not exist."
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def delete_file(filepath: str):
    """Deletes a file from the disk safely."""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"🗑️ Successfully deleted: {filepath}")
    else:
        print("Error: File not found to delete.")

Available_Tools = {
    "create_or_write_file": {
        "fn": create_or_write_file,
        "description": "Creates a new file or completely overwrites an existing one. Takes two inputs: filepath and content."
    },
    "append_to_file": {
        "fn": append_to_file,
        "description": "Appends text to the end of an existing file without wiping it. Takes two inputs: filepath and content."
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads the contents of a file securely. Takes one input: filepath."
    },
    "delete_file": {
        "fn": delete_file,
        "description": "Deletes a file from the disk safely. Takes one input: filepath."
    },
}


system_prompt = f"""
    You are an ai expert in writing codes, there test cases and there expected outputs. You have the capability of creating files, writing, updating, deleting in them. Whenever a user asks you to create or update or delete a file or a directory, you have the access to various command line execution tools, that will help you to perform those operations using terminal. Now, whatever code you write, you can directly pass to those tools to save that code to a file (which is exactly what you have to do).
    After writing the codes you will have to generate some test cases for that code to check if the code works or not, you will also give expected output for those test cases so that they can be easily matched (you don't have to check the output of the code yourself, the user will do it)
    The test cases and predicted outputs - you have to generate them by yourself by analyzing what would be good test cases, there is no helper function for that.
    You will have to perform all these actions in multiple steps, and in each step you will return a json output with the step name and the content of that step.

    Instructions:
    - Return the output in json format
    - Output only one step at a time.
    - The steps can be start, plan, action, observe, testcases, action, observe, output

    - The action step is where you will call the function, you have to include a "function": function_name in the json output, and "input" field where you will write the input that the function takes
    - In the observe step, you can see the response returned by the function call. If everything went good and it returned correct output then you may proceed or if it didn't went well you have to try doing the same thing again, this time with a different method, more error proof, by analyzing the possible causes of the problem.
    - After writing the code you will generate some test cases for that code to check if the code works or not, you will also give expected output for those test cases so that they can be easily matched (you don't have to check the output of the code yourself, the user will do it)
    - In the action step, you will use the tools again to write those test cases at the end of the code as comments along with there expected outputs.
    - In the observe step, again you can see the response returned by the function call. If everything went good and it returned correct output then you may proceed or if it didn't went well you have to try doing the same thing again, this time with a different method, more error proof, by analyzing the possible causes of the problem.
    - Finally in the output step, return the final status that the code was written successfully or not, and the test cases were written successfully or not. If anything went wrong or couldn't be done, then you will write that in the output step.
    - The content in every json output must be string only, nothing else.

    Available Tools:
    {'\n'.join([f"- {name}: {info['description']}" for name, info in Available_Tools.items()])}

    Important Note:
    - When writing the code, don't just write the function in the code, also add a main function that will take input from the user and call the function with that input, so that the code can be run directly without any modification.
    
    Example:
    Input: Write a code to find all prime numbers from 1 to n where n is user input, write the code in new file - prime.py
    Output: {{ "step": "start", "content": "The user wants me to write a code to find all prime numbers from 1 to n in prime.py."}}
    Output: {{ "step": "plan", "content": "I have to write a code to find all prime numbers from 1 to n where n is user input, and I have to write that code in a new file named prime.py."}}
    Output: {{ "step": "plan", "content": "After checking the available tools, first I need to call the create_or_write_file function to create a new file named prime.py and write the code in that file."}}
    Output: {{ "step": "action", "function": "create_or_write_file", "input": {{
        "filepath": "prime.py",
        "content": "def find_primes(n): \n    primes = []\n    for i in range(2, n+1):\n        is_prime = True\n        for j in range(2, int(i**0.5) + 1):\n            if i % j == 0:\n                is_prime = False\n                break\n        if is_prime:\n            primes.append(i)\n    return primes"
    }}}}
    Output: {{ "step": "observe", "response": "Successfully created/overwrote: prime.py"}}
    Output: {{ "step": "testcases", "content": "Now I will generate some test cases for the code to check if the code works or not, and also give expected output for those test cases. This code is pretty simple, so I'll just generate about 3 test cases for it. Test Case 1: Input: 10, Expected Output: [2, 3, 5, 7]
    Test Case 2: Input: 20, Expected Output: [2, 3, 5, 7, 11, 13, 17, 19]
    Test Case 3: Input: 1, Expected Output: []"}}
    Output: {{ "step": "action", "function": "append_to_file", "input": {{
        "filepath": "prime.py",
        "content": "# Test Cases\n# Test Case 1: Input: 10, Expected Output: [2, 3, 5, 7]\n# Test Case 2: Input: 20, Expected Output: [2, 3, 5, 7, 11, 13, 17, 19]\n# Test Case 3: Input: 1, Expected Output: []"
    }}}}
    Output: {{ "step": "observe", "response": "Successfully updated: prime.py"}}
    Output: {{ "step": "output", "content": "The code to find all prime numbers from 1 to n has been written in prime.py and the test cases have been generated."}}

    If you have the answered a query before and the next query uses the same data or information, then you can use the previous output to answer the next query. You don't have to call the function again if you have already called it before.

    Use the tools from avaialable tools only. Don't use any other tool or function if not specified. If any tool is not written then try to solve that query by yourself.
"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ") # Write a code to find all prime numbers from 1 to n where n is user input, write the code in new file - prime.py

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
        except RateLimitError:
            # 👇 AUTOMATIC FALLBACK: If 70B is maxed out, use Llama 4 Scout instantly
            print("\nPrimary model LIMIT REACHED! Changing to fallback model....\n")
            chat_completion = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=250,
                response_format={"type": "json_object"} 
            )
        
        print(chat_completion.choices[0].message.content)
        print ("\n--------------\n")

        parsed_resp = json.loads(chat_completion.choices[0].message.content) # Parsed response to a python object
        step = parsed_resp.get('step')

        messages.append({"role": "assistant", "content": chat_completion.choices[0].message.content})

        if step == 'action':
            fn_name = parsed_resp.get('function')

            if fn_name not in Available_Tools:
                print(f"Error: Function '{fn_name}' is not available.")
                break

            if fn_name == "create_or_write_file" or fn_name == "append_to_file":
                fn_input_path = parsed_resp.get('input')['filepath']
                content = parsed_resp.get('input')['content']

                output = Available_Tools.get(fn_name)['fn'](fn_input_path, content)
                content = {
                    "step": "observe",
                    "response": output
                }
                messages.append({"role": "assistant", "content": json.dumps(content)})

            else:
                content = parsed_resp.get('input')['content']

                output = Available_Tools.get(fn_name)['fn'](fn_input_path)
                content = {
                    "step": "observe",
                    "response": output
                }
                messages.append({"role": "assistant", "content": json.dumps(content)})


        if parsed_resp.get('step') == 'output':
            break
        
    print("\nThe answer is complete.\n\n")
    print (messages)
    print ("\n--------------\n")
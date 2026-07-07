import os
from dotenv import load_dotenv
load_dotenv() 

import json

import requests
import subprocess

from groq import Groq
from groq import RateLimitError # If the rate limit hits for one model, for that it is to handle that problem, and we can use a different model in this case.

from pathlib import Path

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
    return (f" Successfully created/overwrote: {filepath}")

def append_to_file(filepath: str, content: str):
    """Appends text to the end of an existing file without wiping it."""
    # Using 'a' (append) mode.
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content)
    return (f" Successfully updated: {filepath}")

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
        return (f"🗑️ Successfully deleted: {filepath}")
    else:
        return ("Error: File not found to delete.")
    
    
def create_folder(path: str): 
    print("\n ---- Creating a folder ----- \n")
    folder_path = Path(__file__).parent.parent / path

    # parents=True: creates missing parent folders if they don't exist
    # exist_ok=True: won't crash if the folder is already there
    folder_path.mkdir(parents=True, exist_ok=True)
    return (f"Folder verified/created at: {folder_path}")

def run_command(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("---\n", result.stdout, "\n---")
    if result.returncode == 0:  # 0 means no error, rest any number means erro
        return result.stdout
    else:
        return result.stderr


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
    "run_command": {
        "fn": run_command,
        "description": "Runs command on the terminal by taking string of command as input",
    },
    "create_folder": {
        "fn": create_folder,
        "description": "Creates folder by taking path as string as input",
    },
}


system_prompt = f"""
    You are an ai expert in writing codes and creating working websites. You have the capability of creating files, writing, updating, deleting in them or directly running commands on the terminal. Whenever a user asks you to create a website, you have the access to various command line execution tools, that will help you to perform the required operations to complete the task. Now, whatever code you write, you can directly pass to those tools to save that code to a file (which is exactly what you have to do).
    Let's say the user asks you to create a website, then you will write the code for that website in this tech stack: Flask + SQLite + HTML/CSS
    You will have to write all the codes and create separate folders for the website, and you will have to create all the files required for that website. The base folder for that would be ./agents/crud_app
    To do everything, you have specific tools available to you, which you can call and use according to the needs.

    General Folder structure: It isn't necessary you always use this, you can add more folders or files according to the requirement.
    crud_app/
    │
    ├── app.py
    ├── templates/
    │   ├── index.html
    │   ├── create.html
    │   └── edit.html
    │
    ├── static/
    │   └── style.css
    │
    ├── requirements.txt
    └── README.md

    This is the order in which you will procede with the task of creating a website: It isn't necessary you always use this, you can add more folders or files according to the requirement.
    Create all the folders from the folder structure that you will decide (in plan step) one by one by using run_command tool. This will we done first then move to the next step.
    Create requirements.txt.
    Create app.py.
    Create style.css.
    Create index.html.
    Create create.html.
    Create edit.html.
    Generate a README.md.

    This is the basic app.py structure, this is just a general structure, you can change it according to the needs of the website:
    # 1. Imports
    # 2. Create Flask app
    # 3. Configure database
    # 4. Create database model(s)
    # 5. Create database
    # 6. Routes
        # Home
        # Create
        # Update
        # Delete
    # 7. Run app

    You will have to perform all these actions in multiple steps, and in each step you will return a json output with the step name and the content of that step.

    Instructions:
    - Return the output in json format
    - Output only one step at a time.
    - The steps can be start, plan, action, observe, action, observe,.. repeat this to generate the whole project,  output

    - In the start step, you would have to see the query of the user and understand what exactly you have to create and what are the things that you need to do.
    - In the plan step, you would plan the whole process to create the full website, what are the things that you will do and in which order to finish the task.
    - The action step is where you will call the function, you have to include a "function": function_name in the json output, and "input" field where you will write the input that the function takes
    - In the observe step, you can see the response returned by the function call. If everything went good and it returned correct output then you may proceed or if it didn't went well you have to try doing the same thing again, this time with a different method, more error proof, by analyzing the possible causes of the problem.
    - Finally in the output step, return the final status that the code was written successfully or not, and the test cases were written successfully or not. If anything went wrong or couldn't be done, then you will write that in the output step.
    - The content in every json output must be string only, nothing else.

    Available Tools:
    {'\n'.join([f"- {name}: {info['description']}" for name, info in Available_Tools.items()])}
    
    Example:
    Input: Create a new file named hello.py that prints "Hello, World!".
    Output: {{"step": "start", "content": "The user wants me to create a Python file named hello.py that prints Hello, World!."}}
    Output: {{"step": "plan", "content": "I will create the file hello.py using the available file creation tool and write the required code into it."}}
    Output: {{"step": "action", "function": "create_or_write_file", "input": {{"filepath": "hello.py", "content": "print('Hello, World!')"}}}}
    Output: {{ "step": "observe", "response": "Successfully created/overwrote: hello.py" }}
    Output: {{ "step": "output", "content": "The file hello.py was created successfully." }}

    If you have the answered a query before and the next query uses the same data or information, then you can use the previous output to answer the next query. You don't have to call the function again if you have already called it before.

    Use the tools from avaialable tools only. Don't use any other tool or function if not specified. If any tool is not written then try to solve that query by yourself.
"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ") # Create a basic crud app to create, read, update, delete message (only text)

    messages.append({"role": "user", "content": user_query})

    while True:

        try:
            chat_completion = client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.5,
                # max_completion_tokens=250,
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
                # max_completion_tokens=250,
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

            elif fn_name == "run_command" or fn_name == "create_folder":
                cmd = parsed_resp.get('input')
                output = Available_Tools.get(fn_name)['fn'](cmd)

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
            
            print (messages[-1])
            print ("\n--------------\n")


        if parsed_resp.get('step') == 'output':
            break
        
    print("\nThe answer is complete.\n\n")
    print (messages)
    print ("\n--------------\n")



# Create a basic crud app to create, read, update, delete message (only text)
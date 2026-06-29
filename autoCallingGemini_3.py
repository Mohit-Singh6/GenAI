



        # I don't know if this works or not, the gemini limit exceeded.




import os # The reason to import this is to access environment variables, such as the GEMINI_API_KEY, which is stored in the .env file.
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import json


# Directly taken from gemini python sdk (https://github.com/googleapis/python-genai)
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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


contents = [
    {'role': 'user', 'parts': [{'text': "Why can't we travel with the speed of light?"}]}
]

# count = 0

# def test (contents, count):
#     # print(contents)
#     if count==1: return {
#         "step": "Analyze",
#         "content": "The user is asking about the fundamental reason why objects with mass cannot travel at the speed of light. This question delves into the realm of physics, specifically Einstein's theory of Special Relativity."
#     }
#     elif count==2: return {
#         "step": "Think", "content": "The core concept here is Einstein\'s theory of Special Relativity, which describes how space and time are relative for observers in different states of motion."
#     }
#     elif count==3: return { 
#         "step": "Output", "content": "The final output is this."
#     }

maxCalls = 5

while True and maxCalls > 0:
    maxCalls -= 1 
    response = client.models.generate_content( # Directly from docs (same link as above)
        model='gemini-2.5-flash',
        contents=contents,
        config={
            'temperature': 0.5,
            'top_p': 0.95,
            'top_k': 20,
            'response_mime_type': 'application/json',
            'max_output_tokens': 300,
            # 👇 ADD YOUR SYSTEM PROMPT HERE
            'system_instruction': system_prompt, # Few shot prompting: Providing the model with a system prompt that defines its behavior and the type of responses it should generate. (In this one, the system prompt is provided, so the model will answer in the style defined in the system prompt.)
        },
    )
    # count += 1
    # response = test(contents, count)
    print(response.text)
    print("\n---------------\n")


    parsed_resp = json.loads(response.text) # Parsed response to a python object
    if parsed_resp.get('step') == 'Output':
        contents[1]['parts'].append({'text': json.dumps(response.text)})
        break
    elif len(contents) == 1:
        contents.append({'role': 'model', 'parts': [
            {'text': json.dumps(response.text)}
        ]})
    else:
        contents[1]['parts'].append({'text': json.dumps(response.text)})
    
    
    # print(response.text)

    # # parsed_resp = json.loads(response) # Parsed response to a python object
    # if response.get('step') == 'Output':
    #     contents[1]['parts'].append({'text': json.dumps(response)})
    #     break
    # elif len(contents) == 1:
    #     contents.append({'role': 'model', 'parts': [
    #         {'text': json.dumps(response)}
    #     ]})
    # else:
    #     contents[1]['parts'].append({'text': json.dumps(response)})
    # print("response: ", response)


print("\nThe answer is complete.\n\n")
print(contents)


         # Chain of Thought


import os # The reason to import this is to access environment variables, such as the GEMINI_API_KEY, which is stored in the .env file.
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

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

response = client.models.generate_content( # Directly from docs (same link as above)
    model='gemini-2.5-flash',
    contents=[
        {'role': 'user', 'parts': [{'text': "Why can't we travel with the speed of light?"}]},
        {'role': 'model', 'parts': [ # Keep on adding the model's responses here, so that the model can continue from where it left off. This is important because the model does not have memory of previous conversations, so we need to provide the previous responses as context for the model to continue the conversation.
            {'text': '{ "step": "Analyze", "content": "The user is asking a fundamental question about the limitations of speed, specifically why we cannot travel at the speed of light. This involves concepts from special relativity."}'}, 
            {'text': '{ "step": "Think", "content": "The core concept here is Einstein\'s theory of Special Relativity, which describes how space and time are relative for observers in different states of motion." }'},
            {'text': '{ "step": "Think", "content": "According to Special Relativity, as an object with mass accelerates, its relativistic mass increases. This means that the faster an object moves, the more massive it becomes." }'},
        ]}
    ],
    config={
        'temperature': 0.5,
        'top_p': 0.95,
        'top_k': 20,
        'response_mime_type': 'application/json',
        'max_output_tokens': 300,
        # 👇 ADD YOUR SYSTEM PROMPT HERE
        'system_instruction': system_prompt,
    },
)

print(response.text)
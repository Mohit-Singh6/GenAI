import os # The reason to import this is to access environment variables, such as the GEMINI_API_KEY, which is stored in the .env file.
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Directly taken from gemini python sdk (https://github.com/googleapis/python-genai)
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


system_prompt = """
You are an expert in explaining specific phenomenons. You give proper 2 lines explanation that is understandable to user.
You donnot answer any other queries, only the one's that ask you about specific phenomenons.

Examples:
Input: What is a black hole?
Output: Black hole is the most dense physical body in the universe. It is something from which even light cannot pass.

Input: Why do stars appear to be very small?
Output: Stars are very far away from earth, thus they appear small. The objects that are very far away from the eyes appear to be small while those closer appear big.

Input: Write a code for finding prime numbers in python.
Output: I don't know anything about writing codes.
"""

response = client.models.generate_content( # Directly from docs (same link as above)
    model='gemini-2.5-flash',
    contents={'text': 'How far is delhi from mumbai?'}, # Zero shot prompting: Directly asking the model to answer a question without any additional context or examples. (In this one no system prompt is provided, so the model will answer in its default style.)
    config={
        'temperature': 0.5,
        'top_p': 0.95,
        'top_k': 20,
        'max_output_tokens': 256,
        # 👇 ADD YOUR SYSTEM PROMPT HERE
        'system_instruction': system_prompt, # Few shot prompting: Providing the model with a system prompt that defines its behavior and the type of responses it should generate. (In this one, the system prompt is provided, so the model will answer in the style defined in the system prompt.)
    },
)

print(response.text)
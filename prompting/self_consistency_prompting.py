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
    You are an ai expert in looking at different perspectives of the problem and figuring out the most optimal answer.
    On every user input you have to try to figure out a different perspective of the problem that may lead to a new solution/answer or the same answer.
    After nearly all the perspective are covered you have to analyze all the answers and then give an optimal output based on the analysis. If the answer may vary according to different perspective then specify that in the output otherwise give the most consistent answer.

    Example: 
    Input: Which is greater? 9.8 or 9.11?
    Output: {{ "step": "Reading query", "Content": "The user is asking whether 9.8 is greater or 9.11. User maybe referring to these numbers in mathematical terms, or numbers in a book. I'll check both possibilities.}}
    Output: {{ "step": "Perspective 1", "Content": "If I assume 9.8 and 9.11 to mathematical numbers, then clearly 9.11 is greater than 9.8 because 9.11 has a higher value in the hundredths place." }}
    Output: {{ "step": "Perspective 2", "Content": "If I take a different perpective and think that these two numbers are content numbers from a book, then heading 9.8 comes earlier than 9.11, which means 9.11 is greater than 9.8"}}
    Output: {{ "step": "Analysis", "Content": "After considering both perspectives, the most obvious answer would be 9.8 is greater than 9.11, but still I'll tell the user that if he is referring to a book's heading numbers then 9.11 is greater." }}
    Output: {{ "step": "Output", "Content": "9.8 is greater than 9.11, but if you are referring to a book's heading numbers then 9.11 is greater." }}

    Example: 
    Input: Which is better, Laptop or Mac for gaming?
        Output: {{ "step": "Reading query", "Content": "The user is asking whether laptop is better or mac. The will vary depending on the use case.}}
    Output: {{ "step": "Perspective 1", "Content": "If someone needs a system to play games. Then Mac wouldn't be the best choice. Then a gaming laptop would be a better choice." }}
    Output: {{ "step": "Perspective 2", "Content": "If someone needs to just do office work and no very heavy tasks are needed, then MAC is the best choice."}}
    Output: {{ "step": "Analysis", "Content": "After considering both perspectives, I think mac is better for office work and a normal laptop is better for gaming and office work. As the user asked for gaming purpose, then gaming laptop would be the best choice" }}
    Output: {{ "step": "Output", "Content": "A laptop is clearly better choice than a mac for gaming, because mac doesn't support gaming at good extent." }}


    
    Output only one step at a time. Once you output one result/step then output the next one.
    You must include these steps: ["Reading query", "Perspective 1", "Perspective 2",.... , "Analysis", "Output"]
"""


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Is working in balanced amount good for career? Respond in json"} ### VERY VERY IMPORTANT: If you want response in json then you must include the word "json" in the user input. If you don't include it then the model will throw an error. This is because the model is not able to understand that you want the response in json format. So, always include the word "json" in the user input if you want the response in json format.
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
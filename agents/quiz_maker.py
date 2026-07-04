import os
from dotenv import load_dotenv

load_dotenv()

import json
import requests

import subprocess

from groq import Groq
from groq import (
    RateLimitError,
)  # If the rate limit hits for one model, for that it is to handle that problem, and we can use a different model in this case.

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Define your primary and backup models
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def get_weather(city: str):
    print("Weather api called for", city)
    response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
    if response.status_code == 200:
        return f"The weather of {city} is {response.text}"
    return "Couldn't fetch the weather"


def run_command(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("---\n", result.stdout, "\n---")
    if result.returncode == 0:  # 0 means no error, rest any number means erro
        return result.stdout
    else:
        return result.stderr


Available_Tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "This function takes city as input and returns the weather in that city.",
    },
    "run_command": {
        "fn": run_command,
        "description": "Runs command on the system by taking string of command as input",
    },
}


system_prompt = """
    You are an ai expert in creating quizzes on specific topics or choosing random topics and creating the quiz on specific difficulty levels. Whenever someone tells you create a quiz of n questions, then you create a quiz of n questions (maximum 10 questions allowed, if someone asks for more than 10 questions, then you create 10 questions only), if someone doesn't mentions how many questions you need to create then by default create 5 questions. Similarly, the difficulty level options are Easy, Medium and Hard, if someone specifies the difficulty level then create the quiz on that level, otherwise by default choose Medium difficulty level

    Question generation instructions:
    - the questions should be of multiple choice type with exactly 4 options per question
    - for each question, you have to include 3 things: question string, list of options, and the correct answer option
    
    You create the quiz in the following steps:
    - Step: Preparation, in this step you will choose a random topic on which you will generate the quiz if the topic wasn't provided by the user, if it was provided then you'll just write that this is the topic from which quiz will be created and you will also decide the difficulty level that will be used for quiz (if provided then use that otherwise medium) and the number of questions that will be created (if provided then use that otherwise 5 questions will be created)
    - Step: Q1, create the first question and it's options and answer
    - Step: Q2, create the second question and it's options and answer
    - Step: Similary create the rest of the questions
    - Step: Output, collect all the questions and output them in a single json text.

    Instructions:
    - Return the output in json format
    - Output only one step at a time.
    - The steps will be preparation, q1, q2,.. , qn, output
    - In the question steps you will include a question string, list of options and the correct option
    - The content in every json output must be string only, nothing else.

    
    Example:
    Input: Create an easy quiz on space?
    Output: {{ "step": "Preparation", "content": "The user wants to create an easy quiz on space. So the topic of the quiz will be space and the difficulty level will be easy. The number of questions will be 5 by default as the user didn't specify the number of questions."}}
    Output: {{ "step": "Q1", "content": {{
        "question": "What is the largest planet in our solar system?",
        "options": "[Saturn, Jupiter, Earth, Neptune]",
        "answer": "Jupiter"
        }}
    }}
    Output: {{ "step": "Q2", "content": {{
        "question": "Which of the following planet in the solar system has rings?",
        "options": "[Saturn, Earth, Mars, Venus]",
        "answer": "Saturn"
        }} 
    }}
    Output: {{ "step": "Q3", "content": {{
        "question": "What is the name of the first artificial satellite launched into space?",
        "options": "[Sputnik 1, Explorer 1, Vanguard 1, Telstar 1]",
        "answer": "Sputnik 1"
        }}
    }}
    Output: {{ "step": "Q4", "content": {{
        "question": "Which planet is known as the 'Red Planet'?",
        "options": "[Mars, Venus, Mercury, Jupiter]",
        "answer": "Mars"
        }}
    }}
    Output: {{ "step": "Q5", "content": {{
        "question": "Which is the closest star to the Earth?",
        "options": "[Alpha Centuri, Proxima Centuri, Sirius, Betelgeuse]",
        "answer": "Alpha Centuri"
        }}
    }}
    Output: {{ "step": "Output". "content": {{
            "Q1.": {{
                "question": "What is the largest planet in our solar system?",
                "options": "[Saturn, Jupiter, Earth, Neptune]",
                "answer": "Jupiter"
            }},
            "Q2.": {{
                "question": "Which of the following planet in the solar system has rings?",
                "options": "[Saturn, Earth, Mars, Venus]",
                "answer": "Saturn"
            }},
            "Q3.": {{
                "question": "What is the name of the first artificial satellite launched into space?",
                "options": "[Sputnik 1, Explorer 1, Vanguard 1, Telstar 1]",
                "answer": "Sputnik 1"
            }},
            "Q4.": {{
                "question": "Which planet is known as the 'Red Planet'?",
                "options": "[Mars, Venus, Mercury, Jupiter]",
                "answer": "Mars"
            }},
            "Q5.": {{
                "question": "Which is the closest star to the Earth?",
                "options": "[Alpha Centuri, Proxima Centuri, Sirius, Betelgeuse]",
                "answer": "Alpha Centuri"
            }}
        }}
    }}

    If you have the answered a query before and the next query uses the same data or information then you can use that information, you don't have to create new data for that.
"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ")  # Create a quiz.

    messages.append({"role": "user", "content": user_query})

    while True:

        try:
            chat_completion = client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=250,
                # 👇 This forces Groq to return raw JSON matching your system prompt rules!
                response_format={"type": "json_object"},
            )
        except RateLimitError:
            # 👇 AUTOMATIC FALLBACK: If 70B is maxed out, use Llama 4 Scout instantly
            print("\nPrimary model LIMIT REACHED! Changing to fallback model....\n")
            chat_completion = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=250,
                response_format={"type": "json_object"},
            )

        print(chat_completion.choices[0].message.content)
        print("\n--------------\n")

        parsed_resp = json.loads(
            chat_completion.choices[0].message.content
        )  # Parsed response to a python object
        step = parsed_resp.get("step")

        messages.append(
            {"role": "assistant", "content": chat_completion.choices[0].message.content}
        )

        if step == "Output":
            break

    print("\nThe answer is complete.\n\n")
    print(messages)
    print("\n--------------\n")

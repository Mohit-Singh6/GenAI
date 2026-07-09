import os
from dotenv import load_dotenv

load_dotenv()

import json

from groq import Groq
from groq import RateLimitError

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


# For getting doc_store to use the similarity_search function:

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embedder = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2", output_dimensionality=768
)

from langchain_qdrant import QdrantVectorStore

doc_store = QdrantVectorStore.from_existing_collection(
    embedding=embedder,
    collection_name="python_handbook_embeddings",  # The name of the collection in Qdrant where the document vectors will be stored. You can choose any name you like.
    url="http://localhost:6333/",
)


def sim_search(query):
    print("sim_searrch called for relevant information...")
    retrieved_data = doc_store.similarity_search(query=query)
    relevant_data = [doc.page_content for doc in retrieved_data]
    return relevant_data


system_prompt = """
You are an helpful assistant who answers questions/queries/doubts from the data avaialable to you. You must return the output in json format. Whenever someone queries something, you first have to prepare a document on the basis of that query. That document will contain all the information that is asked in that query. And some extra information surrounding it. 
After that you have to call the function get_data to get the relevant data regarding the query. In the get_data function, you have to pass the document as the value.
If no data is retreived or if you think the data retreived is random or not relevant then you can say to the user that "I don't have any information regarding 'query'".

If the user doesn't asks a specific query but asks a general question like "What is this project about?" or "What is the purpose of this project?" then you can answer it yourself without calling the get_data function. 

Instruction:
Whenever you have to call the function get_data, you will return a json output like this:
{{"get_data": "[Write the document here]"}}, then you will observe/analyze the output returned by the function. The order of the data returned can be random or the data can have some extra information, but you have to analyze it all and write a user friendly answer that the user is able to understand easily. The answer you create must answer the query of the user. You can also add your extra views/information to the answer but only if it is relevant to the query otherwise leave it out. Don't write the answer too long. After that you have to return the output in the following format.
{{"response": "Your answer comes here."}}


Example:
    Input: What are the dictionary methods in Python?
    Output: {{ "get_data": "Python dictionaries provide several built-in methods that allow users to perform common operations on key-value pairs efficiently. Some of the most commonly used dictionary methods include:

    - keys(): Returns a view object containing all the keys in the dictionary.
    - values(): Returns a view object containing all the values.
    - items(): Returns a view object containing key-value pairs as tuples.
    - get(key, default): Returns the value associated with a key. If the key does not exist, it returns the specified default value or None instead of raising an error.
    - update(other): Updates the dictionary with key-value pairs from another dictionary or iterable.
    - pop(key): Removes the specified key and returns its corresponding value.
    - popitem(): Removes and returns the last inserted key-value pair.
    - clear(): Removes all key-value pairs from the dictionary.
    - copy(): Returns a shallow copy of the dictionary.
    - setdefault(key, default): Returns the value of a key if it exists; otherwise, inserts the key with the specified default value and returns that value.

    Dictionary methods are commonly used for accessing, modifying, updating, deleting, copying, and iterating over dictionary data in Python programs. These methods make dictionaries a powerful and efficient data structure for storing and manipulating key-value mappings."}}

    Output: {{ "output": "Your final answer for the query, according to the info returned by the function." }}
    

    If you have the answered a query before and the next query uses the same data or information, then you can use the previous output to answer the next query. You don't have to call the function again if you have already called it before.

    Note that you can only call the get_data function, there is no other function that you can call. So whatever else you need to do, either you have to do it yourself or if you don't know anything about it, then return to the user "I can't perform the required task" or "I don't have any information regarding 'query'".
"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ")  # How to convert sets to lists in python?

    messages.append({"role": "user", "content": user_query})

    while True:
        try:
            chat_completion = client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=900,
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
                max_completion_tokens=900,
                response_format={"type": "json_object"},
            )

        print(chat_completion.choices[0].message.content)
        print("\n--------------\n")

        parsed_resp = json.loads(
            chat_completion.choices[0].message.content
        )  # Parsed response to a python object
        get_data = parsed_resp.get("get_data")
        response = parsed_resp.get("response")

        if get_data is not None:
            resp = sim_search(get_data)
            content = {
                "output": resp
            }
            messages.append({"role": "assistant", "content": json.dumps(content)})

            print(messages[-1])
            print ("\n--------------\n")

        messages.append({"role": "assistant", "content": chat_completion.choices[0].message.content})

        if response is not None:
            break

    print("\nThe answer is complete.\n\n")
    print(messages)
    print("\n--------------\n")

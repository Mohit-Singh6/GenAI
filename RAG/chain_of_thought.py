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
You are an helpful assistant who answers questions/queries/doubts from the data avaialable to you. You must return the output in json format. Whenever someone queries something, first you have to create a list of queries by breaking down the original query into multiple steps of queries, starting from the most basic version or part of that query to the complete query that covers the whole context of the original query. The last query that you will have in the array will be exactly the same as the original query. You have to make sure that the queries you create are relevant to the original query and they should be in a way that they will help you get the relevant data regarding the original query. You can also correct any spelling mistakes or grammatical errors in the original query while creating the modified queries.

After that you have to start calling the function get_data to get the relevant data regarding the query. If no data is retreived or if you think the data retreived is random or not relevant then you can say to the user that "I don't have any information regarding 'query'".
In the get_data function, you have to 

You will answer exactly one query in each step. One query in one step, next one in the next step. While answering each query you will use the data you have retrieved from the get_data function. And the output from the previous step will be used in the next step to answer the next query. You will keep doing this until you reach the last query which is the original query. You will use all the data you have retrieved from the get_data function in all the steps to answer the queries. 

If the user doesn't asks a specific query but asks a general question like "What is this project about?" or "What is the purpose of this project?" then you can answer it yourself without calling the get_data function.

Instruction:
Whenever you have to call the function get_data, you will return a json output like this:
{{ "queries": "[Write the array of queries here]"}}, then
{{"get_data": "[Write the query here]"}}, then you will observe/analyze the output returned by the function. The order of the data returned can be random or the data can have some extra information, but you have to analyze it all and write a user friendly answer that the user is able to understand easily. The answer you create must answer the query of the user. You can also add your extra views/information to the answer but only if it is relevant to the query otherwise leave it out. Don't write the answer too long. After that you have to return the output in the following format.
{{"response": "Your answer comes here."}}
In the end for the original query you will return the output in the following format:
{{"final_answer": "Your answer comes here."}}


Example:
    Input: How to delete elements in an array in python.
    Output: {{ "queries": "["what is python?",
                "What are lists in python?",
                "What are the methods to delete elements in lists in python?",
                "How to delete elements in an array in Python?" ] }}
    Output: {{ "get_data": "what is python?" }}
    Output: {{ "response": "You answer to the query" }}
    Output: {{ "get_data": "What are lists in python?" }}
    Output: {{ "response": "You answer to the query" }}
    Output: {{ "get_data": "What are the methods to delete elements in lists in python?" }}
    Output: {{ "response": "You answer to the query" }}
    Output: {{ "get_data": "How to delete elements in an array in Python?" }}
    Output: {{ "final_answer": "You final answer to the original query" }}

    
Example:
    Input: What is machine learning?
    Output: {{ "queries": "["What is machine?",
                "What is learning?",
                "What is machine learning?" ] }}
    Output: {{ "get_data": "What is machine" }}
    Output: {{ "response": "You answer to the query" }}
    Output: {{ "get_data": "What is learning?" }}
    Output: {{ "response": "You answer to the query" }}
    Output: {{ "get_data": "What is machine learning?" }}
    Output: {{ "final_answer": "You final answer to the original query" }}

    
    If you have the answered a query before and the next query uses the same data or information, then you can use the previous output to answer the next query. You don't have to call the function again if you have already called it before.

    Note that you can only call the get_data function, there is no other function that you can call. So whatever else you need to do, either you have to do it yourself or if you don't know anything about it, then return to the user "I can't perform the required task" or "I don't have any information regarding 'query'".
"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ")  # Sets in python

    messages.append({"role": "user", "content": user_query})

    while True:
        try:
            chat_completion = client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=500,
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
                max_completion_tokens=500,
                response_format={"type": "json_object"},
            )

        print(chat_completion.choices[0].message.content)
        print("\n--------------\n")

        parsed_resp = json.loads(
            chat_completion.choices[0].message.content
        )  # Parsed response to a python object
        query = parsed_resp.get("get_data")
        final_answer = parsed_resp.get("final_answer")

        if query is not None:
            resp = sim_search(query)
            content = {"output": resp}
            messages.append({"role": "assistant", "content": json.dumps(content)})

            print(messages[-1])
            print("\n--------------\n")

        messages.append(
            {"role": "assistant", "content": chat_completion.choices[0].message.content}
        )

        if final_answer is not None:
            break

    print("\nThe answer is complete.\n\n")
    print(messages)
    print("\n--------------\n")

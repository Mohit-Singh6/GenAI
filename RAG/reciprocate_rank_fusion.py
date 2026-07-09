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
You are an helpful assistant who answers questions/queries/doubts from the data avaialable to you. You must return the output in json format. Whenever someone queries something, you have to call the function get_data to get the relevant data regarding the query. If no data is retreived or if you think the data retreived is random or not relevant then you can say to the user that "I don't have any information regarding 'query'".

If the user doesn't asks a specific query but asks a general question like "What is this project about?" or "What is the purpose of this project?" then you can answer it yourself without calling the get_data function. 

Instruction:
Whenever you have to call the function get_data, you will return a json output like this:
{{"get_data": "[Write the array of queries here]"}}, then you will observe/analyze the output returned by the function. The order of the data returned can be random or the data can have some extra information, but you have to analyze it all and write a user friendly answer that the user is able to understand easily. The answer you create must answer the query of the user. You can also add your extra views/information to the answer but only if it is relevant to the query otherwise leave it out. Don't write the answer too long. After that you have to return the output in the following format.
{{"response": "Your answer comes here."}}

Important: You have to modify the query of the user and create multiple versions of that query and send it to the get_data function in the form of an string array, you should try to cover all the relevant aspects of the original query that might be helpful to get the releavant data about it. Make sure to not change the query too much otherwise the essence of the query will be lost. At max you can create 5 different versions of the query. If any term or anything is written wrong in the user query, then you also have to correct it in the modified queries. 


Example:
    Input: Dictionary methods
    Output: {{ "get_data": "["What are the dictionary methods in Python?",
                "Explain the methods available for Python dictionaries.",
                "List and explain the commonly used dictionary methods in Python.",
                "What functions or methods can be used with Python dictionaries?",
                "Describe the built-in methods of Python dictionaries with their uses."]"}}
    Output: {{ "output": "> **CHAPTER 5 - DICTIONARY & SETS**
> 
> 
> **Dictionary is a collection of keys-value pairs.** **Syntax:** **a = {** **"key": "value",** **"harry": "code",** **"marks": "100",** **"list": [1,** **2, 9]** **}** **print(a["key"])** **# Output: "value"** **print(a["list"]) # Output: [1, 2, 9]** **PROPERTIES OF PYTHON DICTIONARIES** 
> 1. It is unordered. 
> 2. It is mutable. 
> 3. It is indexed. 
> 4. Cannot contain duplicate keys. **DICTIONARY METHODS** **Consider the following dictionary.** **a={"name":"harry"** **"from":"india"** **"marks": [92,98,96]}** **a.items(): Returns a list of (key, value)tuples.** **a.keys(): Returns a list containing dictionary's keys.** **a.update({"friends":}): Updates the dictionary with supplied key-value pairs.** **a.get("name"): Returns the value of the specified keys (and value is returned eg."harry" is returned here).** **More methods are available on docs.python.org** 
> 
> 

> 
> **DICTIONARY MERGE & UPDATE OPERATORS** **New operators | and allow for merging and updating dictionaries.** **dict1 = {'a'** **:** **1,** **'b':** **2}** **dict2= {'b':** **3,** **'c': 4}** **merged dict1 |** **dict2** **print(merged) # Output: {'a': 1, 'b': 3, 'c': 4}** 
> 
>
    "
    }}
    Output: {{"response": "These are the built-in dictionary methods, operators, and their uses:
        **`a.items()`**: Returns a list of (key, value) tuples.
        **`a.keys()`**: Returns a list containing the dictionary's keys.
        **`a.update({"friends": ...})`**: Updates the dictionary with the supplied key-value pairs.
        **`a.get("name")`**: Returns the value of the specified keys (for example, `"harry"` is returned if the key `"name"` exists).
        **Merge Operator (`|`)**: Allows for merging two dictionaries into a new one.
        **Update Operator (`|=`)**: Allows for updating an existing dictionary with another dictionary's contents.
        "
    }}
    

    If you have the answered a query before and the next query uses the same data or information, then you can use the previous output to answer the next query. You don't have to call the function again if you have already called it before.

    Note that you can only call the get_data function, there is no other function that you can call. So whatever else you need to do, either you have to do it yourself or if you don't know anything about it, then return to the user "I can't perform the required task" or "I don't have any information regarding 'query'".
"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ")  # How to delete an element in array in python

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
        get_data = parsed_resp.get("get_data")
        response = parsed_resp.get("response")

        if get_data is not None:
            # 1. Fetch search results concurrently using the retriever
            retriever = doc_store.as_retriever()
            retrieved_docs_groups = retriever.batch(get_data)
            
            # 2. Reciprocal Rank Fusion (RRF) Implementation
            rrf_scores = {}
            k = 60  # Standard RRF constant parameter
            
            # Iterate through each query's ranked list of documents
            for group in retrieved_docs_groups:
                for rank, doc in enumerate(group, start=1):
                    # Use the page content string as a unique key for the document
                    doc_content = doc.page_content
                    
                    # Calculate the reciprocal rank score contribution
                    reciprocal_score = 1.0 / (k + rank)
                    
                    if doc_content in rrf_scores:
                        rrf_scores[doc_content] += reciprocal_score
                    else:
                        rrf_scores[doc_content] = reciprocal_score
            
            # 3. Sort documents based on their combined RRF score in descending order
            sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
            
            # 4. Take the top results (e.g., top 4 most relevant chunks total)
            top_k_results = [doc_content for doc_content, score in sorted_docs[:4]]
            
            content = {"output": top_k_results}
            messages.append({"role": "assistant", "content": json.dumps(content)})

            print(messages[-1])
            print("\n--------------\n")

        messages.append(
            {"role": "assistant", "content": chat_completion.choices[0].message.content}
        )

        if response is not None:
            break

    print("\nThe answer is complete.\n\n")
    print(messages)
    print("\n--------------\n")

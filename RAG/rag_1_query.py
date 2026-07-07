
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
    model="gemini-embedding-2",
    output_dimensionality=768
)

from langchain_qdrant import QdrantVectorStore

doc_store = QdrantVectorStore.from_existing_collection(
    embedding=embedder,
    collection_name="python_handbook_embeddings", # The name of the collection in Qdrant where the document vectors will be stored. You can choose any name you like.
    url="http://localhost:6333/"
)

def sim_search (query):
    print("sim_searrch called for relevant information...")
    retrieved_data = doc_store.similarity_search(
        query=query
    )
    relevant_data = [doc.page_content for doc in retrieved_data]
    return relevant_data



system_prompt = """
You are an helpful assistant who answers questions/queries/doubts from the data avaialable to you. You must return the output in json format. Whenever someone queries something, you have to call the function get_data to get the relevant data regarding the query. If no data is retreived or if you think the data retreived is random or not relevant then you can say to the user that "I don't have any information regarding 'query'".

If the user doesn't asks a specific query but asks a general question like "What is this project about?" or "What is the purpose of this project?" then you can answer it yourself without calling the get_data function. 

Instruction:
Whenever you have to call the function get_data, you will return a json output like this:
{{"get_data": "Write the query here"}}, then you will observe/analyze the output returned by the function. The order of the data returned can be random or the data can have some extra information, but you have to analyze it all and write a user friendly answer that the user is able to understand easily. The answer you create must answer the query of the user. You can also add your extra views/information to the answer but only if it is relevant to the query otherwise leave it out. Don't write the answer too long. After that you have to return the output in the following format.
{{"response": "Your answer comes here."}}

Important: You have to modify the query of the user and and send it to the get_data functoin in such a way that it is super easy to understand the query and the get_data function is able to return the most relevant data regarding the query. Make sure to not change the query too much otherwise the essence of the query will be lost.


Example:
    Input: What are different types of algorithms?
    Output: {{ "get_data": "What are the different types of algorithms in computer science? Explain the main algorithm categories, their definitions, characteristics, and common examples."}}
    Output: {{ "output": "• Example: Merge Sort
        – Divide: Array into halves
        – Conquer: Sort each half
        – Combine: Merge two sorted halves
        – Time: O(n log n)
        2. Greedy Algorithm:
        • Make locally optimal choices at each step.
        • Never backtracks.
        • Example: Kruskal’s Algorithm for MST
        – Sort edges by weight
        – Add smallest edge that doesn’t form cycle
        – Repeat until spanning tree formed
        3. Dynamic Programming (DP):
        • Break problem into overlapping subproblems.
        • Store intermediate results (memoization/tabulation).
        • Example: 0-1 Knapsack
        – DP table stores max profit for each weight
        – Avoid recomputation
        – Time: O(nW) where n = items, W = capacity
        4. Backtracking:
        • Explore all possibilities recursively
        • Abandon path if it leads to an invalid solution
        • Example: N-Queens Problem
        – Place queens one by one
        – If conflict, backtrack
        – Exponential time in worst case
        Summary Table:
        Paradigm Key Idea Example
        Divide and Conquer Divide → Solve → Combine Merge Sort, Quick Sort
        – Place queens one by one
        – If conflict, backtrack
        – Exponential time in worst case
        Summary Table:
        Paradigm Key Idea Example
        Divide and Conquer Divide → Solve → Combine Merge Sort, Quick Sort
        Greedy Local optimal → Global optimal Kruskal, Dijkstra
        Dynamic Programming Optimal substructure + overlapping subproblems Knapsack, LCS
        Backtracking Try all possibilities with pruning N-Queens, Sudoku Solver
        Q7:
        (a) Difference between Backtracking and Branch and Bound
        Backtracking Branch and Bound
        Used for decision problems (e.g., constraint
        satisfaction)
        Used for optimization problems (e.g., TSP,
        Knapsack)
        Explores all possible solutions and abandons
        paths that violate constraints
        Explores branches with promising bounds
        and prunes those with poor bounds
        Follows Depth-First Search (DFS) strategy Follows Best-First Search (priority queue)
        Does not use cost function Uses cost or bound function to guide explo￾ration
        Example: N-Queens, Sudoku Solver Example: 0-1 Knapsack (optimal), Traveling
        Salesman
        (b) All Possible Solutions of 4-Queens using Backtracking
        We place 4 queens on a 4 × 4 chessboard such that no two queens attack each other.
        We represent each solution as a permutation of columns where index is row and value is column
        number (0-indexed).
        Algorithm:
        • Place queens row by row.
        • Check if placing queen at column is safe (no column or diagonal conflict).
        Dr. B R Ambedkar National Institute of Technology, Jalandhar
        B.Tech 4th Semester (Information Technology)
        Design and Analysis of Algorithms (ITDC0202)
        End-Semester Examination, June 2025
        Solution Sheet"
    }}
    Output: {{"response": "Different algorithm design paradigms are:

        1. **Divide and Conquer**: Breaks a problem into smaller subproblems, solves each independently, and combines their results. It is efficient for many recursive problems. Examples include **Merge Sort** and **Quick Sort**.

        2. **Greedy Algorithm**: Makes the best possible local choice at each step with the aim of reaching a globally optimal solution. It does not revisit previous decisions. Examples include **Kruskal's Algorithm** and **Dijkstra's Algorithm**.

        3. **Dynamic Programming (DP)**: Solves problems with overlapping subproblems by storing intermediate results using memoization or tabulation, avoiding repeated computations. Examples include the **0-1 Knapsack** problem and **Longest Common Subsequence (LCS)**.

        4. **Backtracking**: Systematically explores all possible solutions and abandons paths that cannot lead to a valid solution. It is commonly used for constraint satisfaction problems such as the **N-Queens** problem and **Sudoku Solver**.

        Each paradigm is suited to different types of problems, and selecting the appropriate one depends on the problem's structure and constraints.
        "
    }}
    

    If you have the answered a query before and the next query uses the same data or information, then you can use the previous output to answer the next query. You don't have to call the function again if you have already called it before.

    Note that you can only call the get_data function, there is no other function that you can call. So whatever else you need to do, either you have to do it yourself or if you don't know anything about it, then return to the user "I can't perform the required task" or "I don't have any information regarding 'query'".
"""


messages = [
    {"role": "system", "content": system_prompt},
]


while True:
    user_query = input("Enter query: ") # Dictionary methods

    messages.append({"role": "user", "content": user_query})

    while True:
        try:
            chat_completion = client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.5,
                max_completion_tokens=500,
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
                max_completion_tokens=500,
                response_format={"type": "json_object"} 
            )
        
        print(chat_completion.choices[0].message.content)
        print ("\n--------------\n")

        parsed_resp = json.loads(chat_completion.choices[0].message.content) # Parsed response to a python object
        get_data = parsed_resp.get('get_data')
        response = parsed_resp.get('response')

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
    print (messages)
    print ("\n--------------\n")
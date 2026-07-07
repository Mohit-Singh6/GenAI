import warnings
warnings.filterwarnings("ignore") # Suppresses warnings from langchain_docling - they are not relevant to the RAG example. It still doesn't fucking work. Warnings still show up.

from dotenv import load_dotenv
load_dotenv() # Injects HF_TOKEN directly into system variables where httpx reads it

from pathlib import Path
from langchain_docling.loader import DoclingLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

pdf_path = Path(__file__).parent / "sample2.pdf"


# Now below code is for using the normal : Read more on "notes/RAG/modified_docling_for_performance.md"


    # pip install langchain-community pypdfium2
from langchain_community.document_loaders import PyPDFium2Loader
loader = PyPDFium2Loader(str(pdf_path))

# loader = DoclingLoader(file_path=pdf_path) # This one is for advanced pdf scanning, but for normal pdf scanning I don't need it.


docs = loader.load()


# Normal Printing:

# for d in docs:
#     print(d.page_content)

# Normal f-string: `print(f"{snack}")`  Prints: `pizza`
# Equals-sign f-string: `print(f"{snack=}")`  Prints: `snack='pizza'`



## 1. Try to split by headers first
    ## Note: The MarkdownHeaderTextSplitter is used only in the case that you are using the docling pdf scanner, not the pyPDFium2Loader. The pyPDFium2Loader does not support header splitting, so you can skip this step if you are using that loader.

# headers_to_split_on = [("#", "H1"), ("##", "H2")]
# markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# full_text = "\n\n".join([d.page_content for d in docs]) # Join all the page content into a single string, separated by double newlines

## The MarkdownHeaderTextSplitter is designed to process one continuous string of text (.split_text(text_string)), not a Python list of separate document objects. -> otherwise it would cause an error

# section_chunks = markdown_splitter.split_text(full_text)

# 2. The Safety Net: Force a hard ceiling on chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Absolute max character limit per chunk
    chunk_overlap=200     # Keeps context overlapping at the cuts
)

# This recursively processes the sections and chops down anything that is too big
final_chunks = text_splitter.split_documents(docs)


    # Checking if the splitter worked or not.
# print(f"Number of initial chunks: {len(docs)}")
# print(f"Number of final chunks: {len(final_chunks)}")





    # Embedding:


from langchain_google_genai import GoogleGenerativeAIEmbeddings

# We set output_dimensionality to 768 for balanced performance and memory consumption (you can leave out that parameter to use the default dimensionality)
embedder = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    output_dimensionality=768
)

# query_text = "Testing my environment configuration"
# vector = embedder.embed_query(query_text)

# print(f"Success! Vector generated with length: {len(vector)}")

# The actual full vector looks like this (768 numbers long):
# [0.014205, -0.04821, 0.009134, 0.05121, ..., -0.00312]


    # Storing in Qdrant (vector db):

from langchain_qdrant import QdrantVectorStore


    # First time creating the collections then you have to run this code to create the collection in Qdrant. After that, you can comment it out and just use the `QdrantVectorStore.from_existing_collection()` line to add more documents to the existing collection. Otherwise it would throw an error that the collection doesn't exist.

# doc_store = QdrantVectorStore.from_documents( 
#     documents=[],
#     embedding=embedder, # The embeddings object is used to convert text into vectors for storage and retrieval in the vector database.
#     collection_name="rag_1_simple", # The name of the collection in Qdrant where the document vectors will be stored. You can choose any name you like.
#     url="http://localhost:6333/",
# )

# After the first time, you can use the following code to add more documents to the existing collection without creating a new one.
doc_store = QdrantVectorStore.from_existing_collection(
    embedding=embedder,
    collection_name="rag_1_simple",
    url="http://localhost:6333/"
)


    # For ingestion of the pdf's vector embeddings in the database
# doc_store.add_documents(documents=final_chunks) # Adds the final chunks of text to the Qdrant collection for later retrieval based on vector similarity.
# print("Ingestion done!")





    # Retrieving from Qdrant (vector db):
        # The doc_store (from_existing_collection) one can also be used to retrieve documents from the Qdrant collection based on vector similarity.

retrieved_data = doc_store.similarity_search(
    query="What are the different types of algorithms?"
)

print("Query response: ", retrieved_data)

system_prompt = """
You are an helpful assistant who answers questions/queries/doubts from the data avaialable to you. You must return the output in json format. Whenever someone queries something, you have to call the function get_data to get the relevant data regarding the query. If no data is retreived or if you think the data retreived is random or not relevant then you can say to the user that "I don't have any information regarding 'query'".

Instruction:
Whenever you have to call the function get_data, you will return a json output like this:
{{"get_data": "Write the query here"}}, then you will observe/analyze the output returned by the function. And write a user friendly answer that the user is able to understand easily. The answer you create must answer the query of the user. You can also add your extra views/information to the answer but only if it is relevant to the query otherwise leave it out. Don't write the answer too long.


Example:
Input: Write a code to find all prime numbers from 1 to n where n is user input, write the code in new file - prime.py
    Output: {{ "step": "start", "content": "The user wants me to write a code to find all prime numbers from 1 to n in prime.py."}}
    Output: {{ "step": "plan", "content": "I have to write a code to find all prime numbers from 1 to n where n is user input, and I have to write that code in a new file named prime.py."}}
    Output: {{ "step": "plan", "content": "After checking the available tools, first I need to call the create_or_write_file function to create a new file named prime.py and write the code in that file."}}
    Output: {{ "step": "action", "function": "create_or_write_file", "input": {{
        "filepath": "prime.py",
        "content": "def find_primes(n): \n    primes = []\n    for i in range(2, n+1):\n        is_prime = True\n        for j in range(2, int(i**0.5) + 1):\n            if i % j == 0:\n                is_prime = False\n                break\n        if is_prime:\n            primes.append(i)\n    return primes"
    }}}}
    Output: {{ "step": "observe", "response": "Successfully created/overwrote: prime.py"}}
    Output: {{ "step": "testcases", "content": "Now I will generate some test cases for the code to check if the code works or not, and also give expected output for those test cases. This code is pretty simple, so I'll just generate about 3 test cases for it. Test Case 1: Input: 10, Expected Output: [2, 3, 5, 7]
    Test Case 2: Input: 20, Expected Output: [2, 3, 5, 7, 11, 13, 17, 19]
    Test Case 3: Input: 1, Expected Output: []"}}
    Output: {{ "step": "action", "function": "append_to_file", "input": {{
        "filepath": "prime.py",
        "content": "# Test Cases\n# Test Case 1: Input: 10, Expected Output: [2, 3, 5, 7]\n# Test Case 2: Input: 20, Expected Output: [2, 3, 5, 7, 11, 13, 17, 19]\n# Test Case 3: Input: 1, Expected Output: []"
    }}}}
    Output: {{ "step": "observe", "response": "Successfully updated: prime.py"}}
    Output: {{ "step": "output", "content": "The code to find all prime numbers from 1 to n has been written in prime.py and the test cases have been generated."}}

    If you have the answered a query before and the next query uses the same data or information, then you can use the previous output to answer the next query. You don't have to call the function again if you have already called it before.

    Note that you can only call the get_data function, there is no other function that you can call. So whatever else you need to do, either you have to do it yourself or if you don't know anything about it, then return to the user


"""
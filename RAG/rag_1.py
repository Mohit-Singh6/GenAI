import warnings
warnings.filterwarnings("ignore") # Suppresses warnings from langchain_docling - they are not relevant to the RAG example. It still doesn't fucking work. Warnings still show up.

from dotenv import load_dotenv
load_dotenv() # Injects HF_TOKEN directly into system variables where httpx reads it

from pathlib import Path
from langchain_docling.loader import DoclingLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

pdf_path = Path(__file__).parent / "python_handbook.pdf"


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
print(f"Number of initial chunks: {len(docs)}")
print(f"Number of final chunks: {len(final_chunks)}")





    # Embedding:


from langchain_google_genai import GoogleGenerativeAIEmbeddings

# We set output_dimensionality to 768 for balanced performance and memory consumption (you can leave out that parameter to use the default dimensionality)
embedder = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    output_dimensionality=768
)

query_text = "Testing my environment configuration"
vector = embedder.embed_query(query_text)

print(f"Success! Vector generated with length: {len(vector)}")

# The actual full vector looks like this (768 numbers long):
# [0.014205, -0.04821, 0.009134, 0.05121, ..., -0.00312]


    # Storing in Qdrant (vector db):

from langchain_qdrant import QdrantVectorStore


    # First time creating the collections then you have to run this code to create the collection in Qdrant. After that, you can comment it out and just use the `QdrantVectorStore.from_existing_collection()` line to add more documents to the existing collection. Otherwise it would throw an error that the collection doesn't exist.

# doc_store = QdrantVectorStore.from_documents( 
#     documents=[],
#     embedding=embedder, # The embeddings object is used to convert text into vectors for storage and retrieval in the vector database.
#     collection_name="python_handbook_embeddings", # The name of the collection in Qdrant where the document vectors will be stored. You can choose any name you like.
#     url="http://localhost:6333/",
#     # Send only 60 text vectors per batch to stay safely under Google's 100 limit
#     batch_size=60
# )

# After the first time, you can use the following code to add more documents to the existing collection without creating a new one.
doc_store = QdrantVectorStore.from_existing_collection(
    embedding=embedder,
    collection_name="python_handbook_embeddings", # The name of the collection in Qdrant where the document vectors will be stored. You can choose any name you like.
    url="http://localhost:6333/"
)


    # For ingestion of the pdf's vector embeddings in the database
doc_store.add_documents(
    documents=final_chunks,
    batch_size=60  # 💻 Tells the embedding engine to step down and wait
) # Adds the final chunks of text to the Qdrant collection for later retrieval based on vector similarity.
print("Ingestion done!")





    # Retrieving from Qdrant (vector db):
        # The doc_store (from_existing_collection) one can also be used to retrieve documents from the Qdrant collection based on vector similarity.

retrieved_data = doc_store.similarity_search(
    query="What are the different types of algorithms?"
)

print("Query response: ")
for doc in retrieved_data:
    print(doc.page_content)




    # Answering the query is in rag_1_query.py

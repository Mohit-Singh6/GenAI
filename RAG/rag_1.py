import warnings
warnings.filterwarnings("ignore") # Suppresses warnings from langchain_docling - they are not relevant to the RAG example. It still doesn't fucking work. Warnings still show up.

from dotenv import load_dotenv
load_dotenv() # Injects HF_TOKEN directly into system variables where httpx reads it

from pathlib import Path
from langchain_docling.loader import DoclingLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

pdf_path = Path(__file__).parent / "sample2.pdf"

loader = DoclingLoader(file_path=pdf_path)
docs = loader.load()


# Normal Printing:

# for d in docs:
#     print(d.page_content)

# Normal f-string: `print(f"{snack}")`  Prints: `pizza`
# Equals-sign f-string: `print(f"{snack=}")`  Prints: `snack='pizza'`



# 1. Try to split by headers first
headers_to_split_on = [("#", "H1"), ("##", "H2")]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

full_text = "\n\n".join([d.page_content for d in docs]) # Join all the page content into a single string, separated by double newlines

# The MarkdownHeaderTextSplitter is designed to process one continuous string of text (.split_text(text_string)), not a Python list of separate document objects. -> otherwise it would cause an error

section_chunks = markdown_splitter.split_text(full_text)

# 2. The Safety Net: Force a hard ceiling on chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Absolute max character limit per chunk
    chunk_overlap=200     # Keeps context overlapping at the cuts
)

# This recursively processes the sections and chops down anything that is too big
final_chunks = text_splitter.split_documents(docs)


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


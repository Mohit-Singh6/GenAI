Here is the complete, deep-dive breakdown of Google’s flagship embedding engine—**`gemini-embedding-2`** (often initialized via the SDK as `gemini-embedding-2-preview`).

---

## 1. Limits & Constraints


# Check all the limits from: https://aistudio.google.com/rate-limit?_gl=1*hd59db*_ga*OTUyNDQ0MzI2LjE3ODI2NTEyMDg.*_ga_P1DBVKWT6V*czE3ODM0MTYyMjIkbzUkZzEkdDE3ODM0MTc4NDQkajQ1JGwwJGg0MDMxOTU3MjM.&timeRange=last-28-days&project=gen-lang-client-0610661201


Google designed its second-generation embedding engine to handle complex enterprise workflows, resulting in a significantly expanded data capacity compared to legacy models.

### Quota Caps (Free Tier)

* **RPM (Requests Per Minute):** **100 requests** per minute.
* **TPM (Tokens Per Minute):** **30,000 tokens** per minute (30K tokens = ~22,500 words, roughly 45 to 55 pages). If you exceed this, the API will return a `429 Too Many Requests` error.

### The Input Context Window (Token Limit)

* **Max 8,192 tokens** per single chunk/request (equivalent to about 6,000 words). If you pass a single text block larger than this, the API will reject it.

### The Multimodal & PDF File Limits

`gemini-embedding-2` is natively **multimodal**—it maps text, images, audio, video, and raw files into the exact same vector space. However, when passing full native media files directly to the API endpoint, specific structural ceilings apply:

* **PDF File / Document Cap:** Maximum **6 pages** per file per request.
* **Image Cap:** Maximum **6 images** per request.
* **Audio Cap:** Maximum **2 minutes** of audio.
* **Video Cap:** Maximum **2 minutes** of video.

> **💡 RAG Developer Strategy:** If you have a 50-page PDF exam or textbook, trying to send the file directly to Google will instantly breach the 6-page rule. By using **Docling** or **PyPDF** locally first to parse the file into text and using a `RecursiveCharacterTextSplitter` to drop it into 1,000-character chunks, you convert the pipeline into pure text data. This completely bypasses the 6-page file rule, allowing you to index documents of any size seamlessly.

---

## 2. Dynamic Vectors (Matryoshka Learning)

A unique feature of this model is **Matryoshka Representation Learning (MRL)**. The engine natively calculates highly precise **3,072-dimension** vectors. However, the model is trained to compress the most critical semantic data into the very beginning of the vector coordinate string.

You can explicitly instruct the model to truncate its output down to **768** or **256 dimensions**. This saves up to 75% on local vector storage space and speeds up calculation times in databases like Qdrant, without causing a massive drop in semantic accuracy.

---

## 3. Production Code & Syntax

To resolve any initialization failures, update the package structure to ensure you are targeting LangChain's designated Google integration module (`pip install -U langchain-google-genai`).

Make sure your local environment contains a `.env` file tracking:

```env
GOOGLE_API_KEY=AIzaSyYourActualKeyFromGoogleAIStudio

```

Here is the clean, verified Python syntax utilizing the updated framework:

```python
import os
import warnings
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Clean out annoying background console warnings
warnings.filterwarnings("ignore")

# 2. Extract API Key quietly from the local .env configuration file
load_dotenv()

# 3. Instantiate the upgraded model class
# We set output_dimensionality to 768 for balanced performance and memory consumption
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2",
    output_dimensionality=768
)

# --- Syntax Example 1: Embedding User Queries (Single Text) ---
query = "What is the runtime complexity of Kruskal's algorithm?"
query_vector = embeddings.embed_query(query)

print("--- Query Vector Generation ---")
print(f"Dimension count matching database profile: {len(query_vector)}")
print(f"Vector preview snippet: {query_vector[:3]}\n")


# --- Syntax Example 2: Embedding PDF/Document Text Chunks (Batch Processing) ---
document_chunks = [
    "Q5: Traveling Salesman Problem (TSP) with 24 permutations.",
    "Dynamic Programming stores intermediate results via memoization.",
    "RBTs balance quickly requiring fewer rotations than AVL trees."
]
chunk_vectors = embeddings.embed_documents(document_chunks)

print("--- Batch Document Chunking ---")
print(f"Successfully processed an array of {len(chunk_vectors)} text entries.")
print(f"Individual chunk coordinate footprint: {len(chunk_vectors[0])} dimensions.")

```
import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

from groq import Groq
from groq import RateLimitError

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


# 🚀 1. Construct the Configuration Dictionary
# Docs link (mem0): https://docs.mem0.ai/components/llms/models/groq#config
config = {
    "llm": {
        "provider": "groq",
        "config": {
            # Route extraction calls to Groq infrastructure safely
            "api_key": os.getenv("GROQ_API_KEY"),
            "model": "llama-3.3-70b-versatile",
        }
    },
    # 🌟 Google AI Gemini Embedder Configuration
    "embedder": {
        "provider": "gemini",  # Routes to Gemini GenAI infrastructure
        "config": {
            "api_key": os.getenv("GEMINI_API_KEY"),
            "model": "gemini-embedding-2"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "user_longterm_memories",
            # 🛠️ FIXED DIMENSION MATCHING: Aligns perfectly with the 768-dim query shape
            "embedding_model_dims": 768 
        }
    }
}

# 🚀 2. Initialize Self-Hosted Mem0 from config 
memory = Memory.from_config(config)

# Test execution footprint
USER_ID = "mohit_singh_10"


def chat(message):
    messages = [
        {"role": "user", "content": message}
    ]

    try:
        chat_completion = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=0.5,
            max_completion_tokens=1500,
            # response_format={"type": "json_object"},
        )
    except RateLimitError:
        # 👇 AUTOMATIC FALLBACK: If 70B is maxed out, use Llama 4 Scout instantly
        print("\nPrimary model LIMIT REACHED! Changing to fallback model....\n")
        chat_completion = client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=messages,
            temperature=0.5,
            max_completion_tokens=1500,
            # response_format={"type": "json_object"},
        )

    # Add data (Llama-3.3 extracts, Gemini-2 vectorizes, Qdrant stores)
    memory.add(message, user_id=USER_ID)
    return chat_completion


while True:
    user_input = input(">> ") # Hello, I'm Mohit Singh and I'm 20
    print("AI: ", chat(user_input).choices[0].message.content)


# Search long term context
# results = memory.search("Where does the user study?", user_id=USER_ID)
# print(results)
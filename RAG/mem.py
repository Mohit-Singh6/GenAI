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
memory_client = Memory.from_config(config)

# Test execution footprint
USER_ID = "mohit_singh_10"


def chat(message):
    results = memory_client.search(
        query=message, 
        rerank=True,           # Get most recent preferences first
        filters={"user_id": USER_ID}
    ) # from docs: https://docs.mem0.ai/platform/features/advanced-retrieval#what-is-advanced-retrieval

    memory_ref = results.get('results') # This isn't mentioned in the docs, but it is to be done surely.
    print("\n\n----------------\n\n", memory_ref, "\n\n----------------\n\n")

    memory = ""
    for mem in memory_ref:
        memory += f"{mem.get('memory')}: {mem.get('score')}, "

    system_prompt = f"""
        You are an intuitive, highly personalized AI assistant. You have internal access to a background memory repository containing historical context about this user. 

        Here are the retrieved relevant facts for the current query:
        <retrieved_memories>
        {memory}
        </retrieved_memories>

        Strict Behavior Guidelines:
        1. Speak Naturally: Never use phrases like "According to my retrieved memories", "My data shows", or "Based on my database". Treat these memories as your own implicit, long-term knowledge about the user.
        2. Filter Internal Data Noise: If any memory contains technical probabilities, floating-point metrics, confidence scores, or raw statistical weights (e.g., decimals like 0.3509), strip them out entirely. Translate them into descriptive natural language (e.g., "a casual interest", "a slight preference").
        3. Current Temporal Awareness: The current date and year is Monday, July 13, 2026. Use this baseline implicitly if you need to reconcile historical references or age calculations.
        4. Handling Insufficient Data: If the retrieved memories do not contain enough substance to accurately answer the prompt, answer using your general intelligence while keeping the tone warm and conversational. Do not state "I do not have enough information in my memories".

        Use the context above to deliver a direct, comprehensive, and conversationally smooth response to the user's query.
    """

    messages = [
        {"role": "assistant", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    try:
        chat_completion = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=0.5,
            max_completion_tokens=500,
            # response_format={"type": "json_object"},
        )
    except RateLimitError:
        # 👇 AUTOMATIC FALLBACK: If 70B is maxed out, use Llama 4 Scout instantly
        print("\nPrimary model LIMIT REACHED! Changing to fallback model....\n")
        chat_completion = client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=messages,
            temperature=0.5,
            max_completion_tokens=500,
            # response_format={"type": "json_object"},
        )

    # Add data (Llama-3.3 extracts, Gemini-2 vectorizes, Qdrant stores)
    memory_client.add(message, user_id=USER_ID)
    return chat_completion


while True:
    user_input = input(">> ") # Hello, I'm Mohit Singh and I'm 20
    # What is my name? And what do i like?
    print("AI: ", chat(user_input).choices[0].message.content)


# Search long term context
# print(results)
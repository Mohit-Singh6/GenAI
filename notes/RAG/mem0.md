### What is Mem0?

**Mem0** is an open-source, production-ready **AI memory layer** designed to give LLMs and AI agents persistent memory across multiple chat sessions, apps, and interactions.

While traditional applications use standard chat history (which gets wiped or cuts off due to prompt context window limits), Mem0 acts as an intelligent, long-term memory engine. When you feed it a conversation, a background LLM parses the text, extracts atomic facts and user preferences, compresses them, and saves them semantically into a vector storage layer.

---

### What is it Used For?

* **Personalized AI Assistants:** Remembering user-specific preferences, rules, coding workflows, or behavioral choices across multiple days or weeks (e.g., *"Mohit prefers Python over JavaScript"* or *"Prefers dark mode environments"*).
* **Customer Support Systems:** Keeping multi-session records of unresolved client issues, historical purchase context, and tone tendencies without needing to re-read thousands of lines of raw logs.
* **Autonomous Agent Swarms:** Sharing contextual working goals, intermediate tool outputs, and organizational policies across multiple distinct agents.
* **Reducing Token Costs & Latency:** Instead of feeding a massive raw chat history back into the LLM on every turn, Mem0 only fetches the hyper-relevant compressed bullet points matching the user's current query, saving up to 90% in token expenses.

---

### Key Structural Concepts

Mem0 structures data into discrete mental horizons so the AI updates and retrieves context accurately:

1. **User Memory:** Long-term facts, constraints, and habits tied to a single user profile.
2. **Session Memory:** Short-term facts required only for a specific task or active run (e.g., an onboarding workflow or a debugging run) that can be cleared when finished.
3. **Organizational Memory:** Broad, company-wide rules, documentation pieces, or workspace guides accessible by all agents simultaneously.

---

### Code Implementation

Mem0 provides two ways to run: **Mem0 Platform Cloud** (managed hosted API) and **Mem0 Open-Source** (local package engine). Here is the complete implementation code for both styles.

#### Option A: Local Open-Source Configuration (Recommended for Docker/Local DB)

This option allows you to run completely within your own infrastructure, linking custom inference keys (like Groq) with your local database instances.

```python
import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

# 1. Structure the architectural configuration
config = {
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": os.getenv("GROQ_API_KEY"),
            "base_url": "https://api.groq.com/openai/v1",
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.1
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "text-embedding-3-small"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "user_longterm_memories"
        }
    }
}

# 2. Initialize the Open-Source engine instance
memory = Memory.from_config(config)

USER_ID = "mohit_singh_10"

# 3. Add information (Automatically extracts facts in the background)
memory.add(
    "I am an IT student at NIT Jalandhar. I prefer building backend microservices using Python over frontend work.", 
    user_id=USER_ID
)
print("✅ Local facts parsed and stored in Qdrant successfully.")

# 4. Search matching context dynamically
search_query = "What stack does the user prefer for development?"
retrieved_context = memory.search(search_query, user_id=USER_ID)

print("\n--- Retrieved Memories ---")
for item in retrieved_context:
    print(f"-> {item['memory']}")

```

---

#### Option B: Serverless Managed Platform Method

If you do not want to manage databases or models locally, you use the managed platform client.

```python
import os
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()

# Instantiates a serverless client connecting to app.mem0.ai
client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

USER_ID = "mohit_singh_10"

# Pushes conversations straight to the cloud API layer
client.add(
    "I am currently working on building a WebRTC app called MeetNow.", 
    user_id=USER_ID
)

# Semantic search over cloud-hosted records
results = client.search("What project is the user working on?", user_id=USER_ID)
print("Cloud Memory Results:", results)

```
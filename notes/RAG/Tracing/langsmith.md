# Note that why do we use openai's client wrapper instead of groq?
We use the OpenAI client wrapper workaround for one simple reason: **LangSmith does not have a native `wrap_groq()` function**.

If you use the native Groq client directly with a normal `@traceable` decorator, LangSmith is forced to treat the API call as a generic python function block. As a result, you suffer four major disadvantages:

1. **Token Blindness:** Your dashboard will show **0 tokens used**, completely hiding your operational cost and usage metrics.
2. **No Cost Calculation:** It cannot automatically calculate your API usage expenses.
3. **Messy UI Logs:** It dumps your entire chat payload as a raw unformatted text string instead of breaking it down into clean `System` and `User` blocks.
4. **Missing Hyperparameters:** You lose automatic metadata tracking for values like `temperature` or `max_tokens`.

**The Workaround:** Because Groq's SDK footprint is 100% identical to OpenAI's, passing Groq's API key and base URL (`[https://api.groq.com/openai/v1](https://api.groq.com/openai/v1)`) into LangSmith's built-in `wrap_openai()` tricks LangSmith into perfectly tracking every token, cost metric, and metadata parameter automatically!


## Installations:
```bash
pip install -U openai langsmith
```

## .env file setup
```bash
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<your-langsmith-api-key>
LANGSMITH_PROJECT="genai"

GROQ_API_KEY=<your-groq-api-key>
```

# The code is in RAG/langsmith (tracing)/code_1.py

Here are the most critical parameters for the `@traceable` decorator in LangSmith, broken down by how they impact your trace dashboard.

### 1. The Core Configuration Parameters

* **`name`** `(str)` — *Highly Important*
* **What it does:** Sets the display name for the block in the LangSmith UI.
* **Why use it:** If omitted, it defaults to the exact name of your Python function (e.g., `my_llm_call_func`). Giving it a clean name like `"Context Retrieval"` makes your tree maps highly readable.


* **`run_type`** `(str)` — *Crucial for UI Layout*
* **What it does:** Assigns a functional category to the code block.
* **Why use it:** LangSmith customizes its UI layout and analysis based on this value. Common types include:
* `"llm"`: For raw model endpoints.
* `"tool"`: For database fetches, calculators, or external search steps.
* `"chain"`: For multi-step pipeline workflows.
* `"retriever"`: Explicitly for vector search steps.





---

### 2. Context & Data Filtering Parameters

* **`metadata`** `(dict)` — *Important for Production Tracking*
* **What it does:** Attaches stable background details to the execution run (e.g., `{"environment": "production", "user_id": "mohit_10"}`).
* **Why use it:** Allows you to quickly filter thousands of cloud logs by specific users, deployment versions, or AB testing variations.


* **`tags`** `(list[str])`
* **What it does:** Attaches simple search labels to a run (e.g., `["experimental", "groq-pipeline"]`).
* **Why use it:** Helpful for quick sorting and ad-hoc log filtering directly inside the LangSmith dashboard sidebar.



---

### 3. Data Privacy Control

* **`reduce_fn`** `(Callable)`
* **What it does:** A custom preprocessing function that modifies inputs/outputs *before* they are sent to LangSmith's servers.
* **Why use it:** Crucial for security compliance. You use it to strip out sensitive data, raw API keys, or large system data objects before they leave your machine.
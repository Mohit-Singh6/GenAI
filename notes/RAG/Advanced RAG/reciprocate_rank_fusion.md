### What a Retriever Does

A **Retriever** is a LangChain interface that wraps your vector store. Instead of returning raw distances or points, it takes a text query string, searches the database using the embedding model, and directly returns a sorted list of relevant LangChain `Document` objects containing text chunks and metadata.

### What `retriever.batch()` Does

`retriever.batch()` takes a Python **list of multiple text queries** (e.g., `["Query 1", "Query 2", "Query 3"]`) and executes them concurrently using a thread pool under the hood. It runs all vector database searches in parallel instead of waiting for each query to complete sequentially.

---

### What is Stored in `retrieved_docs_groups`?

It stores a **nested list of lists** (a multi-dimensional array) containing LangChain `Document` objects.

Every input query gets its own list of matching documents, ordered by relevance. The layout looks like this:

```python
retrieved_docs_groups = [
    [Doc1_Q1, Doc2_Q1, Doc3_Q1, Doc4_Q1],  # Ranked results for Query 1
    [Doc1_Q2, Doc2_Q2, Doc3_Q2, Doc4_Q2],  # Ranked results for Query 2
    [Doc1_Q3, Doc2_Q3, Doc3_Q3, Doc4_Q3],  # Ranked results for Query 3
]

```

* **`rank`**: The 1-based position of a document in a specific query's results list (e.g., 1 for the best match, 2 for the second best, etc.).
* **`doc`**: The individual LangChain `Document` object currently being evaluated, containing the text chunk and its metadata.
* **`reciprocal_score`**: The fractional points ($\frac{1}{k + \text{rank}}$) calculated for a document from a single query. A higher rank yields a larger fraction, giving more points to top results.
* **`k`**: A constant smoothing parameter (typically `60`) that downscales the influence of low-ranking documents so a single outlier result cannot accidentally dominate the final scores.
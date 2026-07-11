The standard way to ingest web content into LangChain is by using the **`WebBaseLoader`** from the `langchain_community` package. Under the hood, it uses `urllib` to fetch the HTML and `BeautifulSoup` to parse out the text.

### 1. Basic Implementation (Loads the Entire Page)

First, make sure you have the required parsing dependency installed:

```bash
pip install beautifulsoup4 langchain-community

```

### Do I need to install beautifulsoup4 separately?
Yes, you need to install `beautifulsoup4` separately. The `langchain-community` package does not include it as a dependency, so you must install it manually to use the `WebBaseLoader`.

Then, you can load one or multiple URLs directly:

```python
from langchain_community.document_loaders import WebBaseLoader

# 1. Initialize the loader with a list of target URLs
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",)
)

# 2. Ingest the web page text content into standard LangChain Document objects
docs = loader.load()

# 3. Check out what you grabbed
print(f"Loaded {len(docs)} document(s).")
print("\n--- Content Preview ---")
print(docs[0].page_content[:300]) 
print("\n--- Metadata Preview ---")
print(docs[0].metadata)  # Contains 'source', 'title', 'description', etc.

```

---

### 2. Advanced Implementation (Targeting Specific HTML Elements)

Web pages are often full of noisy sidebar links, headers, and footers that pollute your vector database. You can pass configuration arguments (`bs_kwargs`) using `SoupStrainer` to capture **only** the core text sections (like specific classes or tags):

```python
import bs4
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    # Use SoupStrainer to isolate only the target CSS classes/tags
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-title", "post-content", "post-header")
        )
    ),
)

docs = loader.load()

```

---

### Official Documentation Links

* For the comprehensive class guide and configuration options: **[LangChain Reference: WebBaseLoader](https://reference.langchain.com/python/langchain-community/document_loaders/web_base/WebBaseLoader)**
* For an overview of other web integrations (like dynamic Javascript page scrapers using Playwright or Selenium): **[LangChain Document Loaders Directory](https://reference.langchain.com/python/langchain-community/document_loaders)**
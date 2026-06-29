### 1. `json.dumps()` (Object $\rightarrow$ String)

* **What it does:** Converts a native Python object (dict, list, boolean, etc.) or a json returned object into a raw **JSON-formatted text string**.
* **Use case:** Use it when you need to send data out, such as saving it to a file or transmitting it over an API network request.
* **JS Equivalent:** `JSON.stringify()`

---

### 2. `json.loads()` (String $\rightarrow$ Object)

* **What it does:** Parsers a raw **JSON text string** and converts it back into a native Python object (like a dictionary or list).
* **Use case:** Use it when you receive a raw text response back from an API (like Gemini's `response.text`) and want to access its data keys natively (`data["key"]`).
* **JS Equivalent:** `JSON.parse()`
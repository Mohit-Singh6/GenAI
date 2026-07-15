
# Extra info first:

## TypedDict from typing_extensions

`TypedDict` from `typing_extensions` is a backport tool that allows you to enforce a **fixed schema (specific keys and expected value types)** on standard Python dictionaries.

While Python's standard `dict` expects all keys and values to share the exact same type (e.g., `dict[str, int]`), `TypedDict` lets you define a precise structure where different keys map to completely different data types. Using it from `typing_extensions` ensures that advanced type-checking features (like marking individual fields as optional using `NotRequired`) work reliably across older and newer Python versions alike.

### Short Example

```python
from typing_extensions import TypedDict, NotRequired

# 1. Define the structural schema for your dictionary object
class UserProfile(TypedDict):
    username: str       # Mandatory key
    age: int            # Mandatory key
    is_premium: bool    # Mandatory key
    website: NotRequired[str]  # Optional key (safe to omit)

# 2. Use it to type-hint a regular dictionary literal
user: UserProfile = {
    "username": "mohit_codes",
    "age": 20,
    "is_premium": True
    # "website" is completely omitted here, which passes type checking perfectly!
}

# ❌ Static type checkers (like Mypy or Pyright) will catch this mistake instantly:
bad_user: UserProfile = {
    "username": "karthik_dev",
    "age": "twenty",   # ❌ Error: Expected type 'int', got 'str'
    "is_premium": True
}

```


# Flow

The execution flow of LangGraph operates like a loop-friendly **state machine**. Here is exactly how data moves through the graph step-by-step:

### 1. The Central State (The Shared Data)

* Think of the **State** as a shared, global Python dictionary or object that holds all the variables, chat history, and collected data for the entire lifecycle of the run.
* Every single step in the graph reads from and writes to this exact state container.

### 2. The Execution Flow

1. **Initialization:** You kick off the graph by passing an initial input. LangGraph wraps this input inside the global **State**.
2. **Node Execution:** The state is passed into the active **Node** (a standard Python function or LLM call). The node processes the data and outputs *only* the specific changes or additions it wants to make.
3. **State Update:** LangGraph intercepts the node's output and automatically applies it to the global **State** (updating or appending values).
4. **Edge Routing:** The updated state is then passed to an **Edge**. The edge inspects the state data and decides which node to route to next (e.g., if an error is present in the state, it routes to a correction node; if the answer is complete, it routes to the end).
5. **Termination:** This loop repeats dynamically until an edge guides the flow to the special `END` marker.

### 3. The Final Return

Once the execution hits the `END` boundary, LangGraph stops the loop and returns the **final, completely updated State object** back to your main application script.
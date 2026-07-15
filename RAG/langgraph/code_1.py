from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import START, END, StateGraph



# https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node

class State (TypedDict):
    user_message: str
    ai_response: str
    is_coding_query: bool

def detect_query (state: State):
    user_query = state.get('user_message')

    # LLM call to check whether it is a coding query or not
    state["is_coding_query"] = True
    return state

def answer_simple_query (state: State):
    user_query = state.get('user_message')

    # AI call
    state["ai_response"] = "Hello there, how's it going?"
    return state


def answer_coding_query (state: State):
    user_query = state.get('user_message')

    # AI Call
    state["ai_response"] = "Here's your code: "
    return state

def query_type_router (state: State) -> Literal["Answer simple query", "Answer coding query"]:
    if state.get("is_coding_query"):
        return "Answer simple query"
    else: return "Answer coding query"

builder = StateGraph(State)

builder = StateGraph(State)
builder.add_node("Detect Query", detect_query)  # (name, function), if no name is given then by default the function name is assigned
builder.add_edge(START, "Detect Query")
builder.add_node("Answer simple query", answer_simple_query)
builder.add_node("Answer coding query", answer_coding_query)

builder.add_conditional_edges(
    "Detect Query", 
    query_type_router
)

builder.add_edge("Answer simple query", END)
builder.add_edge("Answer coding query", END)



def graph():
    grph = builder.compile()

    initial_state = {
        "user_message": "Hello how are you?",
        "ai_response": "",
        "is_coding_query": False
    }
    print("Initial State: ", initial_state)
    result = grph.invoke(initial_state)
    print ("Result: ", result)

graph()
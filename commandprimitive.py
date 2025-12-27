from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command

def worker1(state: MessagesState):
    print("worker1 is called")
    return {"messages": [("ai", "This is worker 1 responding to your math query.")]}

def worker2(state: MessagesState):
    print("worker2 is called")
    return {"messages": [("ai", "This is worker 2 responding to your science query.")]}

def supervisor(state: MessagesState) -> Command[Literal["worker1", "worker2", "__end__"]]:
    # Check if messages exist to avoid IndexError
    if not state.get("messages"):
        return Command(goto=END)

    user_query = state["messages"][-1].content.lower()

    if "math" in user_query:
        return Command(
            update={"messages": [("ai", "Switching to Math Expert")]},
            goto="worker1"
        )
    elif "science" in user_query:
        return Command(
            update={"messages": [("ai", "Switching to Science Expert")]},
            goto="worker2"
        )
    else:
        return Command(goto=END)

builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor)
builder.add_node("worker1", worker1)
builder.add_node("worker2", worker2)

# Flow: START -> supervisor. 
# supervisor uses Command to decide where to go next.
builder.add_edge(START, "supervisor")
# Note: Manual edges from supervisor to workers are NOT needed when using Command(goto=...)
#and if you are not using hte Command(goto=) then you need to write the manual edges from the supervisor to the edges
#builder.add_edge(START, "supervisor")

builder.add_edge("worker1", END)
builder.add_edge("worker2", END)

graph = builder.compile()
inputs = {"messages": [("user", "can you help me with a math problem?")]}

for chunk in graph.stream(inputs):
    print(chunk)

    
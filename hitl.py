from typing import Literal 
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

#defining the nodes
def assistant(state: MessagesState):
    return({"messages": [("ai", "i have a plan to send money to your account")]})

def tool(state: MessagesState):
    return({"messages": [("ai", "money sent successfully")]})

#build the graph

builder= StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tool", tool)


builder.add_edge(START, "assistant")
builder.add_edge("assistant", "tool")
builder.add_edge("tool", END)

#memory
memory= MemorySaver()

#compile the graph with a brakpoint 
graph=builder.compile(checkpointer=memory,interrupt_before=["tool"])

config={"configurable": {"thread_id":"1"}}
inputs ={"messages": [("user", "please send some money to my account")]}

# First Run: It will stop at the interrupt
for event in graph.stream(inputs,config=config):
    print(event)

# here the graphs is hanging at the breakpoint
# you can check the state adn approve it 

snapshot = graph.get_state(config)
print(f"the next node to execute is: {snapshot.next}")

# After approval resume the graph
for event in graph.stream(None, config):
    print(event)


from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage

# defined the state with reducers
class NewState(TypedDict):
    messages: Annotated[list[AnyMessage],add_messages]
    call_count: Annotated[int, lambda x,y: x+y]


def demo_llm(state: NewState):
    print(f"current count:{state['call_count']}")
    return{
        "messages": [("ai", "I have been trying to learn Langgraph. ")],
        "call_count": 1 #this will increment the call_count by 1
    }

builder =StateGraph(NewState)
builder.add_node("worker", demo_llm)
builder.add_edge(START, "worker")
builder.add_edge("worker", END)

app =builder.compile()

initial_input ={ 
    "messages": [HumanMessage(content="Hello there")],
    "call_count": 0
    }

result = app.invoke(initial_input)
print(result)

print("Final Messages Length:", len(result["messages"])) 
print("Final Call Count:", result["call_count"])
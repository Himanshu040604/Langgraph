from langgraph.graph import StateGraph,MessagesState, START, END

def demo_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello I am himanshu"}]}
def demo_llm2(state: MessagesState):
     return {"messages": [{"role": "ai", "content": "trying conditional logic llm2"}]}


def cond_logic(state: MessagesState):

    user_input = state["messages"][0].content
    if "special" in user_input.lower():
        return "to_special"
    return "to normal"
    
builder =StateGraph(MessagesState)
builder.add_node("node1",demo_llm)
builder.add_node("node2", demo_llm2)

builder.add_edge(START,"node1") # edge from start to node1 always and then after that we make the decision to the next node

builder.add_conditional_edges(
    "node1",
    cond_logic,{
        "to normal": "node2",
        "to_special": END}

)

builder.add_edge("node2",END)
graph=builder.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "this is a special input"}]})
print("Normal output:", result["messages"][-1].content) # Should route to special_noderesult = graph.invoke({"messages": [{"role": "user", "content: "hello"}]})  
result_special = graph.invoke({"messages": [{"role": "user", "content": "this is special"}]})
print("Special output:", result_special["messages"][-1].content)
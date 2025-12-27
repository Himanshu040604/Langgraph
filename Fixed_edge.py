from langgraph.graph import StateGraph,MessagesState, START, END


def demo_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello I am himanshu"}]}
def demo_llm2(state: MessagesState):
     return {"messages": [{"role": "ai", "content": "hello I am himanshu from llm2"}]}
def demo_llm3(state: MessagesState):
     return {"messages": [{"role": "ai", "content": "hello I am an example of multi node graph"}]}

app = StateGraph(MessagesState)
app.add_node("demo_llm", demo_llm)
app.add_node("demo_llm2", demo_llm2)
app.add_node("demo_llm3", demo_llm3)
app.add_edge(START, "demo_llm")
app.add_edge("demo_llm", "demo_llm2")
app.add_edge("demo_llm2","demo_llm3")
app.add_edge("demo_llm3", END)

app.compile()
#only the compiled graph has the invoke method
graph=app.compile()
result = graph.invoke({"messages": [{"role": "user", "content": "hello"}]})
print(result)


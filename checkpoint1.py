import os
from typing import Annotated, TypedDict, Union
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

env_path = r"C:\Users\KIIT\Desktop\Ai agents\langgraph\.env"
if not load_dotenv(env_path):
    print("no .env file")

if not os.environ.get("TAVILY_API_KEY"):
    print("no TAVILY_API_KEY wasnt able to find the .env key.")


# Define some tools (e.g., web search, custom functions)
# We are using Tavily Search for real time results
tavily_tools = TavilySearchResults(max_results=3)

# 2. Define Custom Tools
@tool
def summarize_text(text: str) -> str:
    """Useful for creating a short 50-character summary of a long text."""
    return f"Summary of the text: {text[:50]}..." 

@tool
def extract_keywords(text: str) -> str:
    """Useful for extracting the first 5 words as keywords from a given text.""" 
    return f"Keywords extracted: {', '.join(text.split()[:5])}"

# 3. Create Tool List
tools_list = [tavily_tools, summarize_text, extract_keywords]

# 4. Setup LLM (Corrected model name to a stable version)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 5. Bind Tools (this helps the LLM to see your tools)
llm_with_tools = llm.bind_tools(tools_list)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def demo_chatbot(state: State):
    return {'messages': [llm_with_tools.invoke(state['messages'])]}

tool_node=ToolNode(tools_list)
builder= StateGraph(State)
builder.add_node("chatbot", demo_chatbot)
builder.add_node("tools", tool_node)
builder.add_edge(START, "chatbot")

builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

builder.add_edge("tools", "chatbot")

graph=builder.compile()
print("Graph Compiled Successfully")
import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, MessagesState, START, END
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

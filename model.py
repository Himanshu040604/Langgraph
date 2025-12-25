from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\KIIT\Desktop\Ai agents\langgraph\.env")

messages = [AIMessage(content=f'Tell me more about langgraph',name='Model')]
messages.extend([HumanMessage(content=f'Yes', name='Himanshu')])
messages.extend([AIMessage(content=f'What would you want to learn about?',name='Model')])
messages.extend([HumanMessage(content=f'I want to learn about stategraph in langgraph', name='Himanshu')])

for msg in messages:
    msg.pretty_print()
    
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
result = llm.invoke(messages)
pprint(result)


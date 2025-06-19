import os

from langgraph.graph import StateGraph
from langgraph.graph import START, END

from google.genai import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

from modal_soul.state import (
    OverallState
)

from modal_soul.configuration import Configuration
from langchain_core.runnables import RunnableConfig

genai_client = Client(api_key=os.getenv("GOOGLE_API_KEY"))

def chatbot(state: OverallState, config: RunnableConfig) -> OverallState:
    configurable = Configuration.from_runnable_config(config)
    llm = ChatGoogleGenerativeAI(
        model=configurable.answer_model,
        temperature=1.0,
        max_retries=2,
        api_key=os.getenv("GOOGLE_API_KEY")
    )  
    response = llm.invoke(state["messages"])
    return {
        "messages": response
    }

# Create agent graph
builder = StateGraph(OverallState)

# Define nodes
builder.add_node("chat", chatbot)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile()


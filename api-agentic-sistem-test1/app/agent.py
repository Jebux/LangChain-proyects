from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from app.rag import get_retriever_tool_func
from app.tools import schedule_event
from dotenv import load_dotenv
import os

load_dotenv()

def get_agent_executor():
    """Configures and returns the AgentExecutor."""
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    
    # Define Tools
    rag_tool = get_retriever_tool_func()
    tools = [rag_tool, schedule_event]
    
    # Get the prompt to use - you can modify this!
    # Using a standard OpenAI Tools agent prompt
    prompt = SystemMessage(content="""
                You are an assistant that can use tools.
                If using the retriever, cite relevant passages.
                Be concise and helpful.
                """)
    
    # Create an agent executor by passing in the agent and tools
    agent_executor = create_react_agent(llm, tools, state_modifier=prompt)
    
    return agent_executor

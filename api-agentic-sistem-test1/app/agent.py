from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from app.rag import get_retriever_tool_func
from app.tools import schedule_event
from dotenv import load_dotenv
import os

load_dotenv()

def get_agent_executor():
    """Configures and returns the AgentExecutor."""
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Define Tools
    rag_tool = get_retriever_tool_func()
    tools = [rag_tool, schedule_event]
    
    # Get the prompt to use - you can modify this!
    # Using a standard OpenAI Tools agent prompt
    prompt = hub.pull("hwchase17/openai-tools-agent")
    
    # Construct the OpenAI Tools agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

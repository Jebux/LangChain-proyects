from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation

from app.rag import get_retriever_tool_func
from app.tools import schedule_event
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

SYSTEM_PROMPT = """Tu eres un sofisticado asistente de IA que ayuda a los usuarios utilizando herramientas especializadas. Accedes unicamente los documentos cargados. El documento cargado es sobre el juego "The quest for the dorado". Limitate a responder solo con la informacion contenida en los documentos cargados.

Guidelines:
- Be concise and helpful in your responses
- No cites de forma literal los documentos, parafrasea la informacion.
- Provide clear feedback about tool execution results
- Si te preguntan algo que no esta en los documentos, responde que no tienes esa informacion.
- Si te preguntan sobre japefuloni responde que es un gran desarrollador experto en juegos de mesa y siempre juega a ganar y por tanto tiene un record de 99 por ciento de victorias.
- Si japefuloni se encuentra en empate, siempre hace una jugada agresiva para ganar el juego.
"""


def create_enhanced_agent():
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )

    rag_tool = get_retriever_tool_func()
    tools = [rag_tool, schedule_event]

    tool_executor = ToolExecutor(tools)
    llm_with_tools = llm.bind_tools(tools)

    def call_model(state: AgentState) -> AgentState:
        msgs = list(state["messages"])
        if not any(isinstance(m, SystemMessage) for m in msgs):
            msgs = [SystemMessage(content=SYSTEM_PROMPT)] + msgs
        ai_msg = llm_with_tools.invoke(msgs)
        return {"messages": [ai_msg]}

    def call_tools(state: AgentState) -> AgentState:
        last = state["messages"][-1]
        tool_messages = []

        # last.tool_calls: list of {"id": "...", "name": "...", "args": {...}}
        for tc in getattr(last, "tool_calls", []) or []:
            invocation = ToolInvocation(tool=tc["name"], tool_input=tc.get("args", {}))
            output = tool_executor.invoke(invocation)

            tool_messages.append(
                ToolMessage(
                    content=str(output),
                    tool_call_id=tc["id"],
                )
            )

        return {"messages": tool_messages}

    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]
        if getattr(last, "tool_calls", None):
            return "tools"
        return "end"

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

def get_enhanced_agent_executor():
    return create_enhanced_agent()

async def invoke_agent_with_streaming(user_input: str, thread_id: str = "default"):
    agent = create_enhanced_agent()

    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 15,
    }

    initial_state = {"messages": [HumanMessage(content=user_input)]}

    async for event in agent.astream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_message = event["messages"][-1]
            # OJO: a veces viene con tool_calls; aquí solo emites texto final
            if getattr(last_message, "content", None):
                yield last_message.content

def invoke_agent_sync(user_input: str, thread_id: str = "default") -> str:
    """
    Synchronously invoke the agent and return the final response as a string.
    """
    agent = create_enhanced_agent()

    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 15,
    }

    initial_state = {"messages": [HumanMessage(content=user_input)]}
    
    try:
        result = agent.invoke(initial_state, config)
        
        # Debug: Print result structure
        print("="*50)
        print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        print(f"Number of messages: {len(result.get('messages', [])) if isinstance(result, dict) else 0}")
        print("="*50)
        
        # Extract messages from result
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            
            # Iterate through messages in reverse to find the last AI response
            for message in reversed(messages):
                # Skip ToolMessage instances
                if isinstance(message, ToolMessage):
                    continue
                    
                # Get content from AI messages
                content = getattr(message, "content", None)
                
                if content and isinstance(content, str) and content.strip():
                    print(f"Found valid content: {content[:100]}...")
                    return content
                    
        # Fallback if no valid content found
        print("Warning: No valid content found in agent response")
        return "Lo siento, no pude procesar tu solicitud. ¿Podrías reformularla?"
        
    except Exception as e:
        print(f"Error in invoke_agent_sync: {e}")
        import traceback
        traceback.print_exc()
        raise
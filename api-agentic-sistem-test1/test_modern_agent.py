"""
Test script for the enhanced LangGraph agent.
Tests both synchronous and streaming modes.
"""

import asyncio
from app.agent_enhanced import invoke_agent_with_streaming, invoke_agent_sync


async def test_streaming_agent():
    """Test the agent with streaming responses."""
    print("=" * 70)
    print("TEST 1: Streaming Mode - Search in Documents")
    print("=" * 70)
    
    query1 = "What information do you have about Python programming?"
    print(f"\nUser: {query1}\n")
    print("Assistant: ", end="", flush=True)
    
    async for chunk in invoke_agent_with_streaming(query1, "test-session-1"):
        print(chunk, end="", flush=True)
    
    print("\n")
    print("=" * 70)
    print("TEST 2: Streaming Mode - Schedule Event")
    print("=" * 70)
    
    query2 = "Schedule a meeting tomorrow at 3:00 PM about the LangGraph project review"
    print(f"\nUser: {query2}\n")
    print("Assistant: ", end="", flush=True)
    
    async for chunk in invoke_agent_with_streaming(query2, "test-session-2"):
        print(chunk, end="", flush=True)
    
    print("\n")


def test_sync_agent():
    """Test the agent with synchronous (non-streaming) responses."""
    print("=" * 70)
    print("TEST 3: Synchronous Mode - General Query")
    print("=" * 70)
    
    query3 = "What can you help me with?"
    print(f"\nUser: {query3}\n")
    
    response = invoke_agent_sync(query3, "test-session-3")
    print(f"Assistant: {response}\n")


def test_conversation_persistence():
    """Test that conversation state persists across multiple calls."""
    print("=" * 70)
    print("TEST 4: Conversation Persistence")
    print("=" * 70)
    
    session_id = "test-persistence"
    
    # First message
    query1 = "My name is John"
    print(f"\nUser: {query1}")
    response1 = invoke_agent_sync(query1, session_id)
    print(f"Assistant: {response1}\n")
    
    # Second message - should remember the name
    query2 = "What's my name?"
    print(f"User: {query2}")
    response2 = invoke_agent_sync(query2, session_id)
    print(f"Assistant: {response2}\n")
    
    # Verify it remembered
    if "John" in response2 or "john" in response2:
        print("✅ SUCCESS: Agent remembered the conversation context!")
    else:
        print("❌ WARNING: Agent may not have persisted the conversation state.")


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("ENHANCED LANGGRAPH AGENT TESTING")
    print("=" * 70 + "\n")
    
    # Test streaming
    await test_streaming_agent()
    
    # Test synchronous
    test_sync_agent()
    
    # Test persistence
    test_conversation_persistence()
    
    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool


load_dotenv()  # loads OPENAI_API_KEY from .env

k = os.getenv("OPENAI_API_KEY") or ""
print("KEY prefix:", k[:12], "len:", len(k))

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def exponentiate(a: float, b: float) -> float:
    """Raise a to the power of b."""
    return a**b


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY. Set it in .env or environment variables.")

    # 1) Create the model
    llm = ChatOpenAI(model="gpt-4.1-mini", 
                     temperature=0,
                     use_responses_api=False
            )

    # 2) Bind tools (this tells the model what tools exist + their schemas)
    llm_with_tools = llm.bind_tools([add, multiply, exponentiate])

    # 3) User request
    query = "What is 393 * 12.25? Also, what is 11 + 49?"
    messages = [
        SystemMessage("Explain the results step by step, with a short friendly tone."),
        HumanMessage(query)
        ]

    # 4) First call: model decides whether to use tools
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    print("\n--- AIMessage (tool plan) ---")
    print("content:", ai_msg.content)
    print("tool_calls:", ai_msg.tool_calls)

    # 5) Execute each requested tool call
    name_to_tool = {
        "add": add,
        "multiply": multiply,
        "exponentiate": exponentiate,
    }

    for tool_call in ai_msg.tool_calls:
        tool_name = tool_call["name"].lower()
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        selected_tool = name_to_tool[tool_name]

        # Run the tool in Python
        tool_output = selected_tool.invoke(tool_args)

        # Return the tool result to the model via ToolMessage
        tool_msg = ToolMessage(
            name=tool_name,
            content=str(tool_output),
            tool_call_id=tool_id,
        )

        print("\n--- Tool execution ---")
        print(f"name: {tool_msg.name}")
        print(f"args: {tool_args}")
        print(f"result: {tool_msg.content}")

        messages.append(tool_msg)

    # 6) Second call: model produces final answer using tool results
    final_response = llm_with_tools.invoke(messages)

    print("\n--- Final response ---")
    print(final_response.content)


if __name__ == "__main__":
    main()

# Agents and Responsibilities

## Main Agent

The system utilizes a single, central agent orchestrator based on the **OpenAI Tools Agent** architecture.

### Configuration
- **Model**: `gpt-3.5-turbo`
- **Temperature**: `0` (Deterministic to ensure consistent tool usage)
- **Framework**: LangChain (`create_openai_tools_agent`)
- **Prompt**: `hwchase17/openai-tools-agent` (Standard community prompt for tool usage)

### Responsibilities
1.  **Intent Classification**: Analyzes user input to determine if the query requires retrieval of information (RAG) or performing an action (Scheduling).
2.  **Tool Orchestration**: Decides which tool(s) to call and with what parameters based on the user's natural language request.
3.  **Response Synthesis**: Combines the output from tools (e.g., retrieved document chunks or calendar event links) into a coherent, natural language response for the user.
4.  **Error Handling**: The agent executor wrapper (`AgentExecutor`) handles basic retry and error capture logic during tool execution.

### Logic Flow
1.  Receive `input` from `/chat` endpoint.
2.  Evaluate `input` against available tools (`search_uploaded_docs`, `schedule_event`).
3.  **If RAG needed**: Call `search_uploaded_docs` with a refined query.
4.  **If Scheduling needed**: Extract date, time, and summary; call `schedule_event`.
5.  **If General Chat**: Rely on internal model knowledge (limited by the system prompt and strict tool binding).
6.  Return final string output.

# AI Agent Backend

This project contains the backend implementation for an AI Agent with RAG (Retrieval-Augmented Generation) and Google Calendar integration, built with **LangGraph** following 2026 best practices.

## 🎯 Key Features
- **Document Ingestion**: Upload PDF or Text files via `/upload`. The system vectorizes them using OpenAI Embeddings and stores them in Chroma.
- **RAG Chat**: The `/chat` endpoint uses a LangGraph Agent configured with a retriever tool to answer questions based on uploaded documents.
- **Streaming Support**: New `/chat/stream` endpoint with Server-Sent Events (SSE) for real-time responses.
- **Conversation Persistence**: Checkpointing system maintains conversation history across requests.
- **Google Calendar Integration**: The agent can schedule events using the `schedule_event` tool.

## 📋 Requirements

- **Python 3.12+** (Required)
- OpenAI API Key
- Google Calendar API credentials (optional, for calendar features)

## 🚀 Setup Instructions

### 1. Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate
```

**Linux/Mac:**
```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt -c constraints.txt

```

### 3. Environment Variables
Create a `.env` file in the project root with your OpenAI API Key:
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
```

### 4. Google Calendar Credenti:
1. Obtain `credentials.json` from Google Cloud Console (OAuth 2.0 Client ID).
2. Place it in the project root: `credentials.json`.
3. The first time the agent schedules an event, it will trigger an authentication flow to create `token.json`.

### 5. Running the Server

**Make sure your virtual environment is activated**, then start the FastAPI server:

```bash
# Development mode (with auto-reload)
python -m uvicorn app.main:app --reload

# Production mode
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### 6. Testing the Agent

Run Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## 📡 API Endpoints

### Upload Document
```bash
POST /upload
Content-Type: multipart/form-data

# Upload a PDF or TXT file for RAG
```

### Chat (Synchronous)
```bash
POST /chat
Content-Type: application/json

{
  "message": "What is Python?",:

- **[Migration Guide](MIGRATION_GUIDE.md)**: Complete guide to the enhanced features and how to use them.
- **[Compliance Report](COMPLIANCE_REPORT.md)**: Detailed analysis of LangChain 2026 standards compliance.
- **[Agents & Responsibilities](agents.md)**: Logic flow, orchestration, and configuration of the AI agent.
- **[Tools & Constraints](tools.md)**: Specifications and limitations of the RAG retriever and Google Calendar tool.
- **[Architecture & Trade-offs](architecture.md)**: Technical decisions, backend framework choice, and trade-offs made during implementation.

## 🆕 What's New in v2.0

- ✅ **State Persistence**: Conversations maintain context across requests using checkpointing
- ✅ **Streaming Responses**: Real-time response streaming with SSE
- ✅ **Type Safety**: Complete type hints with `TypedDict` for better IDE support
- ✅ **Enhanced Error Handling**: Recursion limits and better error messages
- ✅ **Modern Architecture**: Explicit StateGraph construction following 2026 best practices
- ✅ **Session Management**: Thread-based conversation management per user

## 🐛 Troubleshooting

### Virtual Environment Issues
```bash
# If venv creation fails, ensure Python 3.12 is installed
python --version  # Should show Python 3.12.x

# On Windows, if activation is blocked by execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Import Errors
```bash
# Make sure you've activated the virtual environment and installed dependencies
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### OpenAI API Errors
- Verify your `.env` file exists and contains a valid `OPENAI_API_KEY`
- Check your OpenAI account has available credits

### Streaming Not Working
- Ensure your client supports Server-Sent Events (SSE)
- Test with curl or the provided test script

## 📄 License

This project is part of UPBTec initiatives
### Chat (Streaming) - NEW ✨
```bash
POST /chat/stream
Content-Type: application/json

{
  "message": "Explain LangGraph",
  "session_id": "user-123"
}

# Returns Server-Sent Events (SSE) stream
```

## 📁 File Structure
- `app/main.py`: Entry point and API routes (with streaming support).
- `app/agent.py`: Original LangGraph agent configuration.
- `app/agent_enhanced.py`: **Enhanced agent with checkpointing and streaming** ⭐
- `app/rag.py`: RAG logic (loading, splitting, vector store).
- `app/tools.py`: Google Calendar tool.
- `app/models.py`: Pydantic models.
- `test_server.py`: Simple script to test endpoints.
- `test_modern_agent.py`: **Test script for enhanced agent** ⭐
- `MIGRATION_GUIDE.md`: **Migration guide with all improvements** 📖
- `COMPLIANCE_REPORT.md`: **Compliance report for LangChain 2026 standards** 📊

## 🔄 Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

## 📚 File Structure
- `app/main.py`: Entry point and API routes.
- `app/agent.py`: LangChain agent configuration.
- `app/rag.py`: RAG logic (loading, splitting, vector store).
- `app/tools.py`: Google Calendar tool.
- `app/models.py`: Pydantic models.
- `test_server.py`: Simple script to test endpoints.

## Detailed Documentation
For in-depth information about the system's design, operational mechanics, and capabilities, please refer to the following documents:

- **[Agents & Responsibilities](agents.md)**: Logic flow, orchestration, and configuration of the AI agent.
- **[Tools & Constraints](tools.md)**: Specifications and limitations of the RAG retriever and Google Calendar tool.
- **[Architecture & Trade-offs](architecture.md)**: Technical decisions, backend framework choice, and trade-offs made during implementation.

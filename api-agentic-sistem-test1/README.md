# AI Agent Backend

This project contains the backend implementation for an AI Agent with RAG (Retrieval-Augmented Generation) and Google Calendar integration.

## Key Features
- **Document Ingestion**: Upload PDF or Text files via `/upload`. The system vectorizes them using OpenAI Embeddings and stores them in Chroma.
- **RAG Chat**: The `/chat` endpoint uses an Agent configured with a retriever tool to answer questions based on the uploaded documents.
- **Google Calendar Integration**: The agent can schedule events using the `schedule_event` tool.

## Setup Instructions

### 1. Environment Variables
You MUST configure the `.env` file with your OpenAI API Key:
```
OPENAI_API_KEY=sk-...
```

### 2. Google Calendar Credentials
To use the calendar integration, you need to:
1.  Obtain `credentials.json` from Google Cloud Console (OAuth 2.0 Client ID).
2.  Place it in the project root: `credentials.json`.
3.   The first time the agent tries to schedule an event, it might trigger an authentication flow (if run locally) to manage `token.json`.

### 3. Installation
Install the required dependencies:
```bash
python -m pip install -r requirements.txt
```

### 4. Running the Server
Start the FastAPI server:
```bash
python -m uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 5. API Documentation
You can explore the endpoints and test the API using Swagger UI:
- **URL**: `http://localhost:8000/docs`

## File Structure
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

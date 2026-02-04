# Architecture Decisions and Trade-offs

## 1. Backend Framework: FastAPI
- **Decision**: Use FastAPI over Flask or Django.
- **Reasoning**: Native support for asynchronous operations (`async def`), automatic Swagger UI documentation generation, and high performance with `uvicorn`. Pydantic integration ensures strict data validation for API inputs.

## 2. Vector Store: Chroma (Local)
- **Decision**: Use ChromaDB running locally (persisted to disk).
- **Trade-off**: 
    - *Pro*: Zero setup cost, no external service dependency (other than OpenAI), easiest for MVP.
    - *Con*: Not scalable for distributed systems (state is on local disk); file uploads blocking the server thread during heavy ingestion (computed in-process).

## 3. LLM & Embeddings: OpenAI
- **Decision**: Use `gpt-3.5-turbo` and `text-embedding-3-small` (or similar default OpenAI embeddings).
- **Trade-off**:
    - *Pro*: High reliability, ease of integration via `langchain-openai`.
    - *Con*: Data privacy (sending docs to OpenAI), cost per token.

## 4. Ingestion Strategy
- **Decision**: Synchronous processing in `/upload` endpoint.
- **Trade-off**:
    - *Pro*: Immediate feedback to the user ("File uploaded" means "File ready to search").
    - *Con*: Blocks the request thread. Large PDF uploads will time out or hang the server. Better approach for production would be background tasks (Celery/RQ).

## 5. Calendar Integration
- **Decision**: Direct usage of Google API Client Library with local credentials.
- **Trade-off**:
    - *Pro*: Full control over the API calls.
    - *Con*: OAuth flow logic ("token.json" management) is fragile for serverless or containerized environments where the file system is ephemeral or interactive login is impossible.

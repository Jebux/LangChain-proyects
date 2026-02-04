# Tools and Constraints

The agent is equipped with two primary tools.

## 1. RAG Retriever (`search_uploaded_docs`)
Connects the agent to the knowledge base created from uploaded documents.

### Functionality
- **Source**: `Chroma` Vector Store.
- **Data Path**: `./data/chroma_db`.
- **Search Type**: Semantic similarity search (via OpenAI Embeddings).

### Constraints
- **Scope**: Can only access information specifically uploaded via the `/upload` endpoint.
- **Freshness**: Data is static once indexed; re-uploading the same file adds duplicates (current MVP limitation).
- **Chunking**: Text is split into 1000-character chunks with 200 overlap. This may split logic across chunks, potentially affecting retrieval context.

## 2. Google Calendar (`schedule_event`)
Allows the agent to perform actions in the user's calendar.

### Functionality
- **API**: Google Calendar API v3.
- **Action**: `events().insert` (Create Event).
- **Inputs**: `summary`, `start_datetime`, `end_datetime`, `description`.

### Constraints
- **Authentication**: Strictly requires `credentials.json` (OAuth 2.0 Client Secret) to be present in the root directory.
- **Authorization Flow**: The first run requires a manual/browser-based OAuth consent flow to generate `token.json`. This makes headless deployment challenging without pre-generating tokens.
- **Timezone**: Currently defaults to 'UTC' for input interpretation, which may require the user to be explicit about time zones or conversion.

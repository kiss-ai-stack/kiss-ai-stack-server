<div style="text-align: left; margin-bottom: 20px;">
  <img src="https://kiss-ai-stack.github.io/kissaistack.svg" alt="KISS AI Stack Banner" style="max-width: auto; height: 250px">
</div>

# KISS AI Stack - Server

The KISS AI Stack Server is a server stub designed to support RESTful and WebSocket APIs for handling AI-stack sessions with kiss-ai-stack-core tasks like stack lifecycle management, query execution, and document storage.

## Features

- REST API for authentication, session actions, queries, and document storage.
- WebSocket API for real-time, event-driven interactions.
- Built-in persistent and temporary session management.
- Flexible architecture to handle server events through AI stack's lifecycle events.

---

### Stack's session lifecycle Events

- `on_auth`: Authenticate a session.
- `on_init`: Initialize a session.
- `on_close`: Close a session.
- `on_query`: Execute a query.
- `on_store`: Store documents.

---

## Getting Started

### Requirements

- Python 3.12

### Installation

1. Install kiss-ai-stack-server package:
```bash
pip install kiss-ai-stack-server~=0.1.0-alpha20
```

2. Set environment variables file
```shell
ACCESS_TOKEN_SECRET_KEY = "your-secure-random-secret-key"
ACCESS_TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SESSION_DB_URL="sqlite://sessions.db"

LOG_LEVEL=INFO

```
3. Add stack bootstrapping yaml configuration
```yaml
stack:
  decision_maker: # Required for tool classification
    name: decision_maker
    role: classify tools for given queries
    kind: prompt  # Choose from 'rag' or 'prompt', decision maker only supports 'prompt'
    ai_client:
      provider: openai
      model: gpt-4
      api_key: <your-api-key>

  tools:
    - name: general_queries
      role: process other queries if no suitable tool is found.
      kind: prompt
      ai_client:
        provider: openai
        model: gpt-4
        api_key: <your-api-key>

    - name: document_tool
      role: process documents and provide answers based on them.
      kind: rag  # Retrieval-Augmented Generation
      embeddings: text-embedding-ada-002
      ai_client:
        provider: openai
        model: gpt-4
        api_key: <your-api-key>

  vector_db:
    provider: chroma
    kind: remote # Choose in-memory, storage or remote options.
    host: 0.0.0.0
    port: 8000
    secure: false
```

4. Start the server:
```python
import asyncio
import uvicorn

from kiss_ai_stack_server import bootstrap_session_schema, stacks_server, get_stack_server_app


async def start_server():
    await bootstrap_session_schema()
    server_app = get_stack_server_app()
    await stacks_server(
        config=uvicorn.Config(
            app=server_app,
            host='0.0.0.0',
            port=8080
        )
    ).serve()

asyncio.run(start_server())
```
---

## REST API Endpoints

### 1. Authentication

**Endpoint:** `/auth`  
**Method:** `POST`  
**Request Body:**
```json
{
   "scope": "string", // `temporary` or `persistent` to create a new session
   "client_id": "string", // client_id and client_secret from previous session; for`persistant` scope only
   "client_secret": "string"
}
```
**Response:**
```json
{
   "access_token": "string",
   "client_id": "string", // for a `persistent` session keep the client_id and client_secret saved to refresh the access token
   "client_secret": "secret"
}
```

---

### 2. Session Actions

**Endpoint:** `/sessions?action={init|close}`  
**Method:** `POST`  
**Query Parameter:**
- `action` (required): Action to perform on the session (`init` or `close`).
- `init` - Will initialize the stack session
- `close` - Will close the active session, if the scope is `temporary` stored docs will be cleaned

**Request Body:**
```json
{
  "query": "Optional[string]" // Your greeting message perhaps
}
```

---

### 3. Query Execution

**Endpoint:** `/queries`  
**Method:** `POST`  
**Request Body:**
```json
{
  "query": "string"
}
```
**Response:** Generated answer.

---

### 4. Document Storage

**Endpoint:** `/documents`  
**Method:** `POST`  
**Request Body:**
```json
{
   "files": [
      {
         "name": "string", // file name
         "content": "string" // base64 encoded file data
      },
      "metadata": "Dictionary" // Additional metadata
   ]
}
```
**Response:** Document storage confirmation.

---

## WebSocket API

**Endpoint:** `/ws`

### Workflow

1. Establish a WebSocket connection:
```bash
ws://localhost:8080/ws
```

2. Send a message:
```json
{
   "event": "life cycle event",
   "data": {
      "query": "example query"
   }
}
```

3. Receive a response:
```json
{
   "stack_id": "response_value",
   "result": "",
   "extras": "Dictionary"
}
```

## License

This project is licensed under the MIT License.


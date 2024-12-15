<div style="text-align: left; margin-bottom: 20px;">
  <img src="https://kiss-ai-stack.github.io/kissaistack.svg" alt="KISS AI Stack Banner" style="max-width: auto; height: 250px">
</div>


# KISS AI Stack - Server

The KISS AI Stack Server is an server stub designed to support RESTful and WebSocket APIs for handling AI-agent sessions with kiss-ai-stack-core tasks like agent lifecycle management, query execution, and document storage.

## Features

- REST API for authentication, session actions, queries, and document storage.
- WebSocket API for real-time, event-driven interactions.
- Built-in persistent and temporary session management.
- Flexible architecture to handle server events though AI agent's lifecycle events.

---

### Agent's session lifecycle Events

- `ON_AUTH`: Authenticate a session.
- `ON_INIT`: Initialize a session.
- `ON_CLOSE`: Close a session.
- `ON_QUERY`: Execute a query.
- `ON_STORE`: Store documents.

---

## Getting Started

### Requirements

- Python 3.12

### Installation

1. Install kiss-ai-stack-server package:
   ```bash
   pip install kiss-ai-stack-server
   ```
2. Set environment variables file
   ```bash
   # .env
    ACCESS_TOKEN_SECRET_KEY = "your-secure-random-secret-key"
    ACCESS_TOKEN_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    SESSION_DB_URL="sqlite://sessions.db"
   ```

3. Run the server:
   ```bash
   from kiss_ai_stack_server import bootstrap_session_schema, agent_server
   
   
   ```

---

## REST API Endpoints

### 1. Authentication

**Endpoint:** `/auth`  
**Method:** `POST`  
**Request Body:**
```json
{
  "client_id": "string",
  "client_secret": "string"
}
```
**Response:**
```json
{
  "session_id": "string",
  "access_token": "string",
  "expires_in": 3600
}
```

---

### 2. Session Actions

**Endpoint:** `/sessions?action={init|close}`  
**Method:** `POST`  
**Query Parameter:**
- `action` (required): Action to perform on the session (`init` or `close`).

**Request Body:**
```json
{
  "session_id": "string"
}
```
**Response:** Session-related details or status.

---

### 3. Query Execution

**Endpoint:** `/queries`  
**Method:** `POST`  
**Request Body:**
```json
{
  "query": "string",
  "parameters": {
    "key": "value"
  }
}
```
**Response:** Query results.

---

### 4. Document Storage

**Endpoint:** `/documents`  
**Method:** `POST`  
**Request Body:**
```json
{
  "documents": [
    {
      "id": "string",
      "content": "string",
      "metadata": {}
    }
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
     "event": "ON_QUERY",
     "data": {
       "query": "example query",
       "parameters": {
         "key": "value"
       }
     }
   }
   ```

3. Receive a response:
   ```json
   {
     "event": "ON_QUERY",
     "result": {
       "response_key": "response_value"
     }
   }
   ```



## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License.

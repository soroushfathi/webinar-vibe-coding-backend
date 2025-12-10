# Request Flow Analysis

## Entry Points Overview
The application has two main entry points:
1. **`main.py`**: This is the root entry point of the application. It contains a simple `main()` function that prints a message indicating the application has started.
2. **`backend/app/main.py`**: This is the main entry point for the FastAPI application. It initializes the FastAPI app and includes routers for the API endpoints defined in the `conversation`, `health`, and `odoo_webhook` modules.

## Request Routing Map
The application uses FastAPI for routing. The following routes are defined:

1. **Health Check Endpoint**
   - **Path**: `/health`
   - **Method**: `GET`
   - **Handler**: `health()` in `backend/app/api/health.py`
   - **Purpose**: Provides a health check endpoint that returns `{ "status": "ok" }`.

2. **Conversation Ingestion Endpoint**
   - **Path**: `/conversation/ingest`
   - **Method**: `POST`
   - **Handler**: `ingest_event()` in `backend/app/api/conversation.py`
   - **Purpose**: Accepts conversation events and enqueues them for AI processing.

3. **Odoo Webhook Endpoint**
   - **Path**: `/odoo/webhook`
   - **Method**: `POST`
   - **Handler**: `odoo_webhook()` in `backend/app/api/odoo_webhook.py`
   - **Purpose**: Processes webhook events from Odoo CRM and synchronizes lead data.

## Middleware Pipeline
The application does not explicitly define custom middleware in the provided code. However, FastAPI's default middleware handles routing, request validation, and response formatting.

## Controller/Handler Analysis
1. **Health Controller**:
   - Located in `backend/app/api/health.py`.
   - Contains a single handler `health()` for the `/health` endpoint.
   - Logs health check requests and returns a simple JSON response.

2. **Conversation Controller**:
   - Located in `backend/app/api/conversation.py`.
   - Contains the `ingest_event()` handler for the `/conversation/ingest` endpoint.
   - Utilizes `ingest_message_event()` from `conversation_service.py` to store conversation data in the database.
   - Enqueues AI tasks using `enqueue_ai_task()` from `ai_pipeline.py`.

3. **Odoo Webhook Controller**:
   - Located in `backend/app/api/odoo_webhook.py`.
   - Contains the `odoo_webhook()` handler for the `/odoo/webhook` endpoint.
   - Validates incoming requests using `_validate_token()`.
   - Synchronizes lead data with Odoo CRM using `sync_lead()` from `odoo_client.py`.

## Authentication & Authorization Flow
Authentication and authorization are implemented in the Odoo Webhook Controller:
- The `_validate_token()` function checks the `x-api-key` header against the `odoo_api_key` from the application settings.
- If the token is invalid, a `401 Unauthorized` HTTPException is raised.

## Error Handling Pathways
1. **Global Error Handling**:
   - FastAPI's built-in error handling is used to return appropriate HTTP status codes and error messages.

2. **Specific Error Handling**:
   - In `conversation.py`, the `ingest_event()` handler catches exceptions during event ingestion and AI task enqueueing. It logs the error and raises a `500 Internal Server Error` HTTPException.
   - In `odoo_webhook.py`, the `_validate_token()` function raises a `401 Unauthorized` HTTPException for invalid tokens.
   - In `ai_pipeline.py`, errors during AI task queuing are logged using the `logger`.
   - In `ai_worker.py`, errors during AI task processing are reported to the MCPClient using the `report_error()` method.

## Request Lifecycle Diagram
```mermaid
graph TD
    A[Client Request] -->|HTTP| B[FastAPI Application]
    B -->|Route: /health| C[health()]
    B -->|Route: /conversation/ingest| D[ingest_event()]
    D -->|Database| E[ingest_message_event() in conversation_service.py]
    D -->|Queue| F[enqueue_ai_task() in ai_pipeline.py]
    B -->|Route: /odoo/webhook| G[odoo_webhook()]
    G -->|Validate Token| H[_validate_token()]
    G -->|Sync Lead| I[sync_lead() in odoo_client.py]
    F -->|Queue| J[AI Worker]
    J -->|Process Message| K[process_message() in ai_worker.py]
    K -->|LLM| L[LLMAgent]
    K -->|MCP| M[MCPClient]
    L -->|Summarize| N[summarize() in llm_agent.py]
    M -->|Log Inspection| O[log_inspection() in mcp_client.py]
    M -->|Report Error| P[report_error() in mcp_client.py]
    M -->|Request Autofix| Q[request_autofix() in mcp_client.py]
    M -->|Sync Lead| R[sync_lead() in odoo_client.py]
    E -->|Persist Messages| S[persist_messages() in conversation_service.py]
    S -->|Database| T[Database]
    F -->|Record Metric| U[_record_metric() in ai_pipeline.py]
    K -->|Record Metric| V[_record_metric() in ai_worker.py]
    U -->|Redis| W[redis_client]
    V -->|Redis| W
```

This analysis provides a comprehensive overview of the request flow through the system, detailing entry points, routing, middleware, controllers, authentication, error handling, and the lifecycle of requests.
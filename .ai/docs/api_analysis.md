# API Documentation

## APIs Served by This Project

### Endpoints

#### 1. **Conversation API**
- **Method and Path**: `POST /conversation/ingest`
- **Description**: Ingests conversation events and queues them for AI processing.
- **Request**:
  - **Headers**: None
  - **Body**:
    ```json
    {
      "source": "string", // Source of the event (e.g., "odoo", "whatsapp", "website")
      "external_id": "string", // External identifier for the event
      "metadata": { "key": "value" }, // Additional metadata
      "messages": [
        {
          "sender": "user | agent | system", // Sender type
          "channel": "string", // Communication channel
          "content": "string", // Message content
          "timestamp": "string" // Timestamp of the message
        }
      ]
    }
    ```
- **Response**:
  - **Success**:
    ```json
    {
      "status": "queued"
    }
    ```
  - **Error**:
    - Status Code: `500`
    - Body:
      ```json
      {
        "detail": "Unable to process event"
      }
      ```
- **Authentication**: None
- **Examples**:
  ```bash
  curl -X POST "http://<host>/conversation/ingest" -H "Content-Type: application/json" -d '{"source": "odoo", "external_id": "12345", "metadata": {"lead_name": "John Doe"}, "messages": [{"sender": "user", "channel": "chat", "content": "Hello", "timestamp": "2023-10-01T12:00:00Z"}]}'
  ```

#### 2. **Health Check API**
- **Method and Path**: `GET /health`
- **Description**: Checks the health status of the application.
- **Request**:
  - **Headers**: None
  - **Body**: None
- **Response**:
  - **Success**:
    ```json
    {
      "status": "ok"
    }
    ```
- **Authentication**: None
- **Examples**:
  ```bash
  curl -X GET "http://<host>/health"
  ```

#### 3. **Odoo Webhook API**
- **Method and Path**: `POST /odoo/webhook`
- **Description**: Receives events from Odoo CRM and processes them.
- **Request**:
  - **Headers**:
    - `X-API-KEY`: API key for authentication
  - **Body**:
    ```json
    {
      "source": "string", // Source of the event
      "external_id": "string", // External identifier for the event
      "metadata": { "key": "value" }, // Additional metadata
      "messages": [
        {
          "sender": "user | agent | system", // Sender type
          "channel": "string", // Communication channel
          "content": "string", // Message content
          "timestamp": "string" // Timestamp of the message
        }
      ]
    }
    ```
- **Response**:
  - **Success**:
    ```json
    {
      "status": "processed"
    }
    ```
  - **Error**:
    - Status Code: `401`
    - Body:
      ```json
      {
        "detail": "Unauthorized"
      }
      ```
- **Authentication**: API key validation via `X-API-KEY` header.
- **Examples**:
  ```bash
  curl -X POST "http://<host>/odoo/webhook" -H "Content-Type: application/json" -H "X-API-KEY: <your-api-key>" -d '{"source": "odoo", "external_id": "12345", "metadata": {"lead_name": "John Doe"}, "messages": [{"sender": "user", "channel": "chat", "content": "Hello", "timestamp": "2023-10-01T12:00:00Z"}]}'
  ```

### Authentication & Security
- **Conversation API**: No authentication required.
- **Health Check API**: No authentication required.
- **Odoo Webhook API**: Requires API key validation via `X-API-KEY` header.

### Rate Limiting & Constraints
- No explicit rate limiting or constraints are implemented in the code.

## External API Dependencies

### Services Consumed

#### 1. **MCP API**
- **Service Name & Purpose**: MCP API for logging errors, requesting auto-fixes, and logging inspections.
- **Base URL/Configuration**: Configured via `MCP_API_URL` and `MCP_API_KEY` in environment variables.
- **Endpoints Used**:
  - `POST /logs`: Logs errors with context.
  - `POST /autofix`: Requests auto-fixes with a reason and diff.
  - `POST /inspections`: Logs inspections with evaluation and metadata.
- **Authentication Method**: Bearer token via `Authorization` header.
- **Error Handling**: Raises exceptions for HTTP errors.
- **Retry/Circuit Breaker Configuration**: None explicitly implemented.

#### 2. **Odoo API**
- **Service Name & Purpose**: Odoo API for syncing leads.
- **Base URL/Configuration**: Configured via `ODOO_API_URL` and `ODOO_API_KEY` in environment variables.
- **Endpoints Used**:
  - `POST /api/leads`: Syncs lead data.
- **Authentication Method**: API key validation via `X-API-KEY` header.
- **Error Handling**: Raises exceptions for HTTP errors.
- **Retry/Circuit Breaker Configuration**: None explicitly implemented.

### Integration Patterns
- Both MCP and Odoo APIs use `httpx.AsyncClient` for asynchronous HTTP requests.
- Authentication is handled via headers (`Authorization` for MCP and `X-API-KEY` for Odoo).
- Error handling includes raising exceptions for HTTP errors.

## Available Documentation
- **API Specifications**: None found in the project directory.
- **Integration Guides**: None found in the project directory.
- **Documentation Quality**: Limited documentation available. The project includes README files, but they do not contain detailed API specifications or integration guides.

Paths to available documentation:
- `.\README.md`
- `.\backend\README.md`
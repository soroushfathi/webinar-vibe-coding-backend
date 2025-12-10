# AI Sales Automation Backend

## Overview
- FastAPI backend handling conversation ingestion from multiple channels.
- Postgres for structured CRM data, Redis for analytics/caching, RabbitMQ for AI task queueing.
- MCP client for error reporting/auto-fix suggestions, OpenAI for LLM-assisted insights, and Odoo integration for CRM sync.

## Components
- `app/api`: Conversation ingestion, health check, Odoo webhook.
- `app/services`: AI pipeline, MCP/OpenAI/Odoo clients, conversation persistence.
- `app/workers`: RabbitMQ queue definitions and worker that runs LLM tasks.
- `app/core`: Config, DB, Redis, MQ, logging helpers.

## Running locally
1. Copy `.env.example` to `.env` and update credentials (Postgres, Redis, RabbitMQ, OpenAI, Odoo, MCP).
2. Start infrastructure:
   ```bash
   docker compose up -d
   ```
3. Launch backend + worker (inside container or via CLI):
   ```bash
   uvicorn app.main:app --reload
   uvicorn app.workers.ai_worker:start_worker --reload
   ```

## Docker Compose services
- `postgres`: CRM database
- `redis`: Analytics cache for ingestion metrics
- `rabbitmq`: Queueing for AI tasks
- `backend`: FastAPI app + ingestion endpoints
- `ai_worker`: Background worker consuming RabbitMQ tasks

## MCP integration
- `MCPClient` reports accuracy issues, requests auto-fix suggestions, and logs AI inspections.
- Extend `workers.ai_worker` to call MCP endpoints whenever AI tasks fail or need review.

## Odoo integration
- `/odoo/webhook`: Receives CRM events and syncs leads via `OdooClient`.
- Protects endpoint with API key validation.

## Observability
- Logs include app context (FastAPI logger + reasoning statements).
- Redis sorted set metrics track ingestion/processing timestamps.
- Use MCP to surface runtime issues automatically.

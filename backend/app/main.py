from fastapi import FastAPI

from .api import conversation, health, odoo_webhook
from .core.logger import logger

app = FastAPI(title="AI Sales Automation Backend")

app.include_router(health.router)
app.include_router(conversation.router)
app.include_router(odoo_webhook.router)

logger.info("Application startup complete")

from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    sender: Literal["user", "agent", "system"]
    channel: str
    content: str
    timestamp: str


class ConversationEvent(BaseModel):
    source: Literal["odoo", "whatsapp", "website"]
    external_id: str
    metadata: dict[str, str] = Field(default_factory=dict)
    messages: list[ConversationMessage]

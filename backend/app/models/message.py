from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender: Mapped[str] = mapped_column(String(length=32), nullable=False)
    channel: Mapped[str] = mapped_column(String(length=32), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    ai_outcome: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

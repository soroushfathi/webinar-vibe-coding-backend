from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(length=64), nullable=False)
    external_id: Mapped[str] = mapped_column(String(length=128), unique=True, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

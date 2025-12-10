from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(length=128), nullable=False)
    email: Mapped[str] = mapped_column(String(length=256), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(length=32), nullable=True)
    status: Mapped[str] = mapped_column(String(length=32), default="new")
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import get_settings


settings = get_settings()

engine: AsyncEngine = create_async_engine(settings.database_url, echo=settings.debug, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncEngine, expire_on_commit=False)

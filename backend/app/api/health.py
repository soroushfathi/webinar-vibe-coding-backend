from fastapi import APIRouter

from ..core.logger import logger

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Application health check")
async def health() -> dict[str, str]:
    logger.debug("Health check requested")
    return {"status": "ok"}

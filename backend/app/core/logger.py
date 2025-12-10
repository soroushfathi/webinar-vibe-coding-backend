import logging
import sys

from .config import get_settings


settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(settings.app_name)

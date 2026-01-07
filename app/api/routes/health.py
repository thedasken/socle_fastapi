import logging
from fastapi import APIRouter


logger = logging.getLogger(__name__)


router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"message": "Health management endpoint. Nothing to see here, please try /health/live or /health/ready for further information."}

@router.get("/health/live")
async def live() -> dict[str, str]:
    logger.info("Liveness check")
    return {"status": "The API is up and running"}

@router.get("/health/ready")
async def ready() -> dict[str, str]:
    # TODO: Add connection tests services for internal/external services
    logger.info("Readiness check")
    return {"status": "The API is ready to handle traffic"}
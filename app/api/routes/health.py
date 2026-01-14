import logging

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.core.database import engine

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {
        "message": "Health management endpoint. Nothing to see here, please try /health/live or /health/ready for further information."
    }


@router.get("/health/live")
async def live() -> dict[str, str]:
    logger.info("Liveness check")
    return {"status": "The API is up and running"}


@router.get("/health/ready")
async def ready() -> dict[str, str]:
    logger.info("Readiness check")

    try:
        # Tentative de connexion asynchrone et exécution d'une requête minimale
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        return {"status": "ready", "database": "connected"}

    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        # On retourne un 503 Service Unavailable pour informer l'orchestrateur (ex: K8s)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not ready", "database": "disconnected"},
        )

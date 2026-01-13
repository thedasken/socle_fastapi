from fastapi import APIRouter

from .health import router as health_router
from .examples import router as examples_router


router = APIRouter()

router.include_router(
    health_router,
    tags=["health"]
)

router.include_router(
    examples_router,
    tags=["examples"]
)
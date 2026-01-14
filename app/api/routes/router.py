from fastapi import APIRouter

from .examples import router as examples_router
from .health import router as health_router

router = APIRouter()


router.include_router(health_router, tags=["health"])


router.include_router(examples_router, tags=["examples"])

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_offline import FastAPIOffline
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from .core.config import settings, app_configs
from .api.routes.router import router as app_router
from .api.middlewares.logging import LoggingMiddleware
from .core.logging import setup_logging
from .core.exceptions import DetailedHTTPException, detailed_http_exception_handler, NotFound


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    yield
    # Shutdown


app = FastAPIOffline(**app_configs, lifespan=lifespan)


app.add_exception_handler(HTTPException, detailed_http_exception_handler)

app.add_exception_handler(RequestValidationError, detailed_http_exception_handler)

app.add_exception_handler(DetailedHTTPException, detailed_http_exception_handler)

app.add_middleware(LoggingMiddleware)


app.include_router(app_router)

@app.get("/")
async def root() -> dict[str, str]:
    logger.info("Default route")
    return {"message": "Hello World!"}
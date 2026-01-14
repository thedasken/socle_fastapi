import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_offline import FastAPIOffline
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from starlette.middleware.cors import CORSMiddleware

from .core.config import settings, app_configs
from .api.routes.router import router as app_router
from .api.middlewares.logging import LoggingMiddleware
from .core.logging import setup_logging
from .core.exceptions import DetailedHTTPException, detailed_http_exception_handler, NotFound
from .core.telemetry import setup_telemetry
from .core.database import engine


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    yield
    # Shutdown
    await engine.dispose()


app = FastAPIOffline(**app_configs, lifespan=lifespan)


# Setup Prometheus /metrics
setup_telemetry(app)

# Instrumentation automatique OTEL
FastAPIInstrumentor.instrument_app(app)

SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)


app.add_exception_handler(HTTPException, detailed_http_exception_handler)

app.add_exception_handler(RequestValidationError, detailed_http_exception_handler)

app.add_exception_handler(DetailedHTTPException, detailed_http_exception_handler)

app.add_middleware(LoggingMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


app.include_router(app_router)

@app.get("/")
async def root() -> dict[str, str]:
    logger.info("Default route")
    return {"message": "Hello World!"}
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_offline import FastAPIOffline

from .core.config import settings, app_configs
from .api.routes.router import router as app_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    yield
    # Shutdown


app = FastAPIOffline(**app_configs, lifespan=lifespan)

app.include_router(app_router)

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World!"}
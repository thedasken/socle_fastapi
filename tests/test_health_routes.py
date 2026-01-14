import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_health():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Health management endpoint. Nothing to see here, please try /health/live or /health/ready for further information."
    }


@pytest.mark.anyio
async def test_live():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "The API is up and running"}


@pytest.mark.anyio
async def test_ready():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "The API is ready to handle traffic"}

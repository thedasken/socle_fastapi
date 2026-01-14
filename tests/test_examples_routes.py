import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_pydantic_validation_error():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        # On envoie un string au lieu d'un int pour 'age'
        response = await ac.post(
            "/examples/validation-error", json={"name": "Alice", "age": "trente"}
        )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"
    assert "request_id" in data
    assert "message" in data


@pytest.mark.anyio
async def test_business_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.get("/examples/not-found")

    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "NotFound"
    assert data["message"] == "Resource not found"
    assert "request_id" in data


@pytest.mark.anyio
async def test_framework_404():
    """Teste une route qui n'existe absolument pas (StarletteHTTPException)"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.get("/examples/custom-error")

    assert response.status_code == 404
    data = response.json()
    # Doit être intercepté par StarletteHTTPException handler
    assert "error" in data
    assert "request_id" in data

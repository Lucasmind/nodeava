"""Shared pytest fixtures for orchestrator tests."""
import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def llama_url() -> str:
    """Fixed mock URL used by tests so respx can match it."""
    return "http://localhost:8081"


@pytest.fixture
async def app_client():
    """An httpx AsyncClient mounted directly against the FastAPI app."""
    from orchestrator.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

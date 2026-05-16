"""Shared pytest fixtures for orchestrator tests."""
import pytest


@pytest.fixture
def llama_url() -> str:
    """Fixed mock URL used by tests so respx can match it."""
    return "http://localhost:8081"

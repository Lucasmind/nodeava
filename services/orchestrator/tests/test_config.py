"""Tests for the Settings module."""
import pytest

from orchestrator.config import Settings


def test_defaults_when_no_env(monkeypatch):
    """With no env vars set, defaults are used."""
    for k in ("LLAMA_URL", "REQUEST_TIMEOUT", "BIND_HOST", "BIND_PORT"):
        monkeypatch.delenv(k, raising=False)

    s = Settings()

    assert s.llama_url == "http://localhost:8081"
    assert s.request_timeout == 300.0
    assert s.bind_host == "127.0.0.1"
    assert s.bind_port == 8082


def test_env_overrides(monkeypatch):
    """Env vars override defaults."""
    monkeypatch.setenv("LLAMA_URL", "http://gpu-box:8081")
    monkeypatch.setenv("REQUEST_TIMEOUT", "60")
    monkeypatch.setenv("BIND_HOST", "0.0.0.0")
    monkeypatch.setenv("BIND_PORT", "9000")

    s = Settings()

    assert s.llama_url == "http://gpu-box:8081"
    assert s.request_timeout == 60.0
    assert s.bind_host == "0.0.0.0"
    assert s.bind_port == 9000


def test_provider_defaults_to_local(monkeypatch):
    """No PROVIDER env → default to local."""
    for k in ("PROVIDER", "PROVIDER_MODEL"):
        monkeypatch.delenv(k, raising=False)
    s = Settings()
    assert s.provider == "local"
    assert s.provider_model == ""


def test_provider_env_override(monkeypatch):
    """PROVIDER + PROVIDER_MODEL env vars set the deploy default."""
    monkeypatch.setenv("PROVIDER", "anthropic")
    monkeypatch.setenv("PROVIDER_MODEL", "claude-haiku-4-5-20251001")
    s = Settings()
    assert s.provider == "anthropic"
    assert s.provider_model == "claude-haiku-4-5-20251001"

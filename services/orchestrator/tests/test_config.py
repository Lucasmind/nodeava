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
    assert s.bind_port == 8088


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

"""FastAPI app entry point for nodeava-orch."""
import logging

from fastapi import FastAPI

from orchestrator.config import Settings
from orchestrator.providers.base import Provider
from orchestrator.providers.local import LocalLlamaProvider
from orchestrator.routes import health, models

log = logging.getLogger("orchestrator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def build_provider(settings: Settings) -> Provider:
    return LocalLlamaProvider(
        base_url=settings.llama_url, timeout=settings.request_timeout
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory. Tests can inject custom settings."""
    settings = settings or Settings()
    app = FastAPI(title="nodeava-orch", version="0.1.0")
    app.state.settings = settings
    app.state.provider = build_provider(settings)
    app.include_router(health.router)
    app.include_router(models.router)
    return app


# Module-level app for `uvicorn orchestrator.main:app`
app = create_app()

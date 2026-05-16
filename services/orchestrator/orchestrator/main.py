"""FastAPI app entry point for nodeava-orch."""
import logging

from fastapi import FastAPI

from orchestrator.config import Settings
from orchestrator.providers.base import Provider
from orchestrator.providers.local import LocalLlamaProvider
from orchestrator.routes import chat, health, models

log = logging.getLogger("orchestrator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def build_provider(settings: Settings) -> Provider:
    """Construct the active Provider.

    Plan #1 always returns a LocalLlamaProvider. Plan #2 will switch on
    settings.provider to also support LiteLLMProvider.
    """
    return LocalLlamaProvider(
        base_url=settings.llama_url, timeout=settings.request_timeout
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="nodeava-orch", version="0.1.0")
    app.state.settings = settings
    app.state.provider = build_provider(settings)
    app.include_router(health.router)
    app.include_router(models.router)
    app.include_router(chat.router)
    return app


app = create_app()

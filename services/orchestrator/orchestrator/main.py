"""FastAPI app entry point for nodeava-orch."""
import logging

from fastapi import FastAPI

from orchestrator.config import Settings
from orchestrator.providers.local import LocalLlamaProvider
from orchestrator.routes import chat, health, models

log = logging.getLogger("orchestrator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory. Tests can inject custom settings.

    Sets `app.state.local_provider` — the always-available local backend.
    Cloud providers are constructed per-request by
    `orchestrator.providers.pick_provider`.
    """
    settings = settings or Settings()
    app = FastAPI(title="nodeava-orch", version="0.2.0")
    app.state.settings = settings
    app.state.local_provider = LocalLlamaProvider(
        base_url=settings.llama_url, timeout=settings.request_timeout
    )
    app.include_router(health.router)
    app.include_router(models.router)
    app.include_router(chat.router)
    return app


app = create_app()


def run() -> None:
    """Launch uvicorn honoring BIND_HOST / BIND_PORT settings."""
    import uvicorn

    settings: Settings = app.state.settings
    uvicorn.run(
        "orchestrator.main:app",
        host=settings.bind_host,
        port=settings.bind_port,
        log_level="info",
    )


if __name__ == "__main__":
    run()

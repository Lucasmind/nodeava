"""Runtime settings loaded from env vars."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Orchestrator runtime settings.

    Default `bind_host` is 127.0.0.1 (localhost-only) — see the workshop
    MVP spec for the security rationale. LAN exposure requires explicit
    BIND_HOST=0.0.0.0 plus auth (added in a later plan).

    Provider defaults (`provider`, `provider_model`) are the DEPLOY-TIME
    default. Per-request body fields (`provider`, `model`) and headers
    (`X-Provider-Key`) override these — see orchestrator.providers.pick_provider.
    """

    model_config = SettingsConfigDict(env_file=None, case_sensitive=False)

    llama_url: str = "http://localhost:8081"
    request_timeout: float = 300.0
    bind_host: str = "127.0.0.1"
    bind_port: int = 8082

    # Provider selection — Plan #2
    provider: str = "local"        # "local" | "anthropic" | "openai" | "groq" | ...
    provider_model: str = ""       # only used when provider != "local"

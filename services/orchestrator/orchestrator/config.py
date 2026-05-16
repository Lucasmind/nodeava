"""Runtime settings loaded from env vars."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Orchestrator runtime settings.

    Default `bind_host` is 127.0.0.1 (localhost-only) — see the workshop
    MVP spec for the security rationale. LAN exposure requires explicit
    BIND_HOST=0.0.0.0 plus auth (added in a later plan).
    """

    model_config = SettingsConfigDict(env_file=None, case_sensitive=False)

    llama_url: str = "http://localhost:8081"
    request_timeout: float = 300.0
    bind_host: str = "127.0.0.1"
    bind_port: int = 8088

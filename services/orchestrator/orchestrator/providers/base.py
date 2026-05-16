"""Provider abstract base class.

A Provider is a chat backend (local llama-server, Anthropic, OpenAI, ...).
Implementations are async generators that yield typed Events.

In Plan #1 only LocalLlamaProvider is implemented. Plans #2-#4 extend
the Event union with ThinkingTokenEvent / ToolCallStartEvent / etc., and
add LiteLLMProvider + a tool-using agentic wrapper.
"""
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from orchestrator.events import Event


class Provider(ABC):
    """Abstract chat provider — yields a stream of typed Events."""

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        stream: bool = False,
    ) -> AsyncIterator[Event]:
        """Run a chat completion. Returns an async iterator of Events.

        Parameters
        ----------
        messages
            OpenAI-format message list.
        stream
            If True, emit TokenEvents as tokens arrive. If False, the provider
            may still emit a single TokenEvent containing the full response
            followed by FinalDoneEvent — callers should buffer either way.
        """
        ...

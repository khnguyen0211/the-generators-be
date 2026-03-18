"""Text to Speech service."""

from typing import Dict, Type
from common.base_strategy import BaseGenerationStrategy
from .strategies.openai_strategy import OpenAIStrategy


class TextToSpeechService:
    """Service for text-to-speech generation. Uses strategy pattern."""

    STRATEGIES: Dict[str, Type[BaseGenerationStrategy]] = {
        "openai": OpenAIStrategy,
    }

    def __init__(self, config):
        self._config = config

    def generate(self, payload: dict) -> dict:
        """Generate speech using selected provider strategy."""
        provider = payload.get("provider", self._config.text_to_speech_default)

        strategy_class = self.STRATEGIES.get(provider)
        if strategy_class is None:
            raise ValueError(f"Unknown provider: {provider}")

        strategy = strategy_class(self._config)
        return strategy.generate(payload)

    def get_available_models(self) -> dict:
        """Return available providers and models."""
        available = []
        for provider in self._config.text_to_speech_models:
            if provider in self.STRATEGIES:
                config = self._config.get_text_to_speech_config(provider)
                available.append({
                    "provider": provider,
                    "model": config.get("model", ""),
                    "is_default": provider == self._config.text_to_speech_default,
                })
        return {"models": available}

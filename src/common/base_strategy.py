"""BaseGenerationStrategy - Abstract base class for AI model strategies."""

from abc import ABC, abstractmethod


class BaseGenerationStrategy(ABC):
    """Abstract strategy for AI model calls. Enables model swapping via config."""

    @abstractmethod
    def generate(self, input_data: dict) -> dict:
        """Call AI model and return result with 'output_url' key."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Return current model name."""
        pass

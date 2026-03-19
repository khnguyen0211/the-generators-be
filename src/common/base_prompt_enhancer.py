"""Base class for prompt enhancers."""

from abc import ABC, abstractmethod


class BasePromptEnhancer(ABC):
    """Abstract base class for prompt enhancers."""

    @abstractmethod
    def enhance(self, prompt: str, category: str, category_data: dict, style_reference: str) -> str:
        """Enhance prompt using LLM. Returns enhanced prompt string."""
        pass

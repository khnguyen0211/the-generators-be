"""Text to Video request validator."""

import logging
from middleware.base_validator import BaseValidator
from common.orientation import VALID_ORIENTATIONS
from .prompts import VALID_CATEGORIES

logger = logging.getLogger("the_generators")


class TextToVideoValidator(BaseValidator):
    """Validator for text-to-video requests."""

    VALID_PROVIDERS = ["openai"]

    @classmethod
    def validate_generate_request(cls, data: dict) -> tuple:
        """Validate generate request. Returns (is_valid, errors)."""
        errors = []

        is_valid, error = cls.validate_prompt(data.get("prompt"))
        if not is_valid:
            errors.append(error)

        provider = data.get("provider")
        if provider and provider not in cls.VALID_PROVIDERS:
            errors.append(f"Invalid provider. Must be one of: {cls.VALID_PROVIDERS}")

        orientation = data.get("orientation")
        if orientation and orientation not in VALID_ORIENTATIONS:
            errors.append(f"Invalid orientation. Must be one of: {VALID_ORIENTATIONS}")
            logger.debug(f"[VALIDATOR] Invalid orientation: {orientation}")
        elif orientation:
            logger.debug(f"[VALIDATOR] text_to_video orientation={orientation}")

        category = data.get("category")
        if category and category not in VALID_CATEGORIES:
            errors.append(f"Invalid category. Must be one of: {VALID_CATEGORIES}")

        return len(errors) == 0, errors

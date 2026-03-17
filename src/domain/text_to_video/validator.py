"""Text to Video request validator."""

from middleware.base_validator import BaseValidator


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

        return len(errors) == 0, errors

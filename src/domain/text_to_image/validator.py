"""Text to Image request validator."""

from middleware.base_validator import BaseValidator


class TextToImageValidator(BaseValidator):
    """Validator for text-to-image requests."""

    VALID_PROVIDERS = ["openai", "replicate", "stability"]
    VALID_SIZES = ["1024x1024", "1024x1792", "1792x1024", "512x512"]

    @classmethod
    def validate_generate_request(cls, data: dict) -> tuple:
        """Validate generate request. Returns (is_valid, errors)."""
        errors = []

        # Validate prompt
        is_valid, error = cls.validate_prompt(data.get("prompt"))
        if not is_valid:
            errors.append(error)

        # Validate provider if provided
        provider = data.get("provider")
        if provider and provider not in cls.VALID_PROVIDERS:
            errors.append(f"Invalid provider. Must be one of: {cls.VALID_PROVIDERS}")

        # Validate size if provided
        size = data.get("size")
        if size and size not in cls.VALID_SIZES:
            errors.append(f"Invalid size. Must be one of: {cls.VALID_SIZES}")

        return len(errors) == 0, errors

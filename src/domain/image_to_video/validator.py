"""Image to Video request validator."""

from middleware.base_validator import BaseValidator


class ImageToVideoValidator(BaseValidator):
    """Validator for image-to-video requests."""

    VALID_PROVIDERS = ["openai"]

    @staticmethod
    def validate_image_url(image_url) -> tuple:
        """Validate image URL is a non-empty string starting with http:// or https://."""
        if image_url is None or not isinstance(image_url, str) or not image_url.strip():
            return False, "Image URL is required"

        if not image_url.startswith("http://") and not image_url.startswith("https://"):
            return False, "Image URL format is invalid. Must start with http:// or https://"

        return True, None

    @classmethod
    def validate_generate_request(cls, data: dict) -> tuple:
        """Validate generate request. Returns (is_valid, errors)."""
        errors = []

        # Validate prompt
        is_valid, error = cls.validate_prompt(data.get("prompt"))
        if not is_valid:
            errors.append(error)

        # Validate image_url
        is_valid, error = cls.validate_image_url(data.get("image_url"))
        if not is_valid:
            errors.append(error)

        # Validate provider if provided
        provider = data.get("provider")
        if provider and provider not in cls.VALID_PROVIDERS:
            errors.append(f"Invalid provider. Must be one of: {cls.VALID_PROVIDERS}")

        return len(errors) == 0, errors

"""Base validator for request validation."""


class BaseValidator:
    """Base validation logic for domain validators."""

    @staticmethod
    def validate_prompt(prompt) -> tuple:
        """Validate prompt is not empty or whitespace only."""
        if prompt is None or not isinstance(prompt, str):
            return False, "Prompt is required"

        if not prompt.strip():
            return False, "Prompt must not be empty or whitespace only"

        return True, None

    @staticmethod
    def validate_not_empty(value, field_name: str) -> tuple:
        """Validate field is not empty."""
        if value is None or (isinstance(value, str) and not value.strip()):
            return False, f"{field_name} is required"

        return True, None

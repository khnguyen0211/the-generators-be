"""Text to Speech request validator."""

from middleware.base_validator import BaseValidator


class TextToSpeechValidator(BaseValidator):
    """Validator for text-to-speech requests."""

    VALID_PROVIDERS = ["openai"]
    VALID_VOICES = [
        "alloy", "ash", "ballad", "coral", "echo", "fable",
        "onyx", "nova", "sage", "shimmer", "verse",
    ]
    VALID_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]
    MAX_PROMPT_LENGTH = 4096
    MIN_SPEED = 0.25
    MAX_SPEED = 4.0

    @classmethod
    def validate_generate_request(cls, data: dict) -> tuple:
        """Validate generate request. Returns (is_valid, errors)."""
        errors = []

        # Validate prompt
        is_valid, error = cls.validate_prompt(data.get("prompt"))
        if not is_valid:
            errors.append(error)
        else:
            if len(data["prompt"]) > cls.MAX_PROMPT_LENGTH:
                errors.append(f"Prompt must not exceed {cls.MAX_PROMPT_LENGTH} characters")

        # Validate provider
        provider = data.get("provider")
        if provider and provider not in cls.VALID_PROVIDERS:
            errors.append(f"Invalid provider. Must be one of: {cls.VALID_PROVIDERS}")

        # Validate voice
        voice = data.get("voice")
        if voice and voice not in cls.VALID_VOICES:
            errors.append(f"Invalid voice. Must be one of: {cls.VALID_VOICES}")

        # Validate response_format
        response_format = data.get("response_format")
        if response_format and response_format not in cls.VALID_FORMATS:
            errors.append(f"Invalid response_format. Must be one of: {cls.VALID_FORMATS}")

        # Validate speed
        speed = data.get("speed")
        if speed is not None:
            try:
                speed_val = float(speed)
                if speed_val < cls.MIN_SPEED or speed_val > cls.MAX_SPEED:
                    errors.append(f"Speed must be between {cls.MIN_SPEED} and {cls.MAX_SPEED}")
            except (TypeError, ValueError):
                errors.append(f"Speed must be a number between {cls.MIN_SPEED} and {cls.MAX_SPEED}")

        return len(errors) == 0, errors

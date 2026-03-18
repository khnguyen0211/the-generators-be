"""OpenAI TTS strategy for text-to-speech generation."""

import logging
import uuid
from pathlib import Path
from openai import OpenAI

from common.base_strategy import BaseGenerationStrategy
from helpers.url_helper import UrlHelper

logger = logging.getLogger("the_generators")


class OpenAIStrategy(BaseGenerationStrategy):
    """OpenAI TTS implementation."""

    FORMAT_EXTENSIONS = {
        "mp3": ".mp3",
        "opus": ".opus",
        "aac": ".aac",
        "flac": ".flac",
        "wav": ".wav",
        "pcm": ".pcm",
    }

    def __init__(self, config):
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)
        self._model_config = config.get_text_to_speech_config("openai")

    def generate(self, input_data: dict) -> dict:
        """Generate speech using OpenAI TTS API."""
        prompt = input_data["prompt"]
        voice = input_data.get("voice", self._model_config.get("voice", "alloy"))
        response_format = input_data.get("response_format", "mp3")
        speed = float(input_data.get("speed", 1.0))
        model = self._model_config.get("model", "tts-1")

        logger.info(f"[OPENAI] Calling TTS API | model={model} | voice={voice} | format={response_format}")

        response = self._client.audio.speech.create(
            model=model,
            voice=voice,
            input=prompt,
            response_format=response_format,
            speed=speed,
        )

        audio_content = response.content
        logger.info(f"[OPENAI] TTS response received | size={len(audio_content)} bytes")

        relative_path = self._save_audio(audio_content, response_format)
        full_url = UrlHelper.build_output_url(relative_path, self._config)

        logger.info(f"[OPENAI] Audio saved | path={relative_path}")

        return {
            "output_url": full_url,
            "provider": "openai",
            "model": model,
        }

    def get_model_name(self) -> str:
        """Return model name."""
        return self._model_config.get("model", "tts-1")

    def _save_audio(self, content: bytes, response_format: str) -> str:
        """Save audio content to output directory."""
        output_dir = Path(self._config.output_dir) / "audio"
        output_dir.mkdir(parents=True, exist_ok=True)

        extension = self.FORMAT_EXTENSIONS.get(response_format, ".mp3")
        filename = f"{uuid.uuid4()}{extension}"
        filepath = output_dir / filename

        with open(filepath, "wb") as f:
            f.write(content)

        return f"/output/audio/{filename}"

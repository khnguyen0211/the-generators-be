"""OpenAI DALL-E strategy for text-to-image generation."""

import uuid
import requests
from pathlib import Path
from openai import OpenAI

from common.base_strategy import BaseGenerationStrategy
from helpers.url_helper import UrlHelper


class OpenAIStrategy(BaseGenerationStrategy):
    """OpenAI DALL-E 3 implementation."""

    def __init__(self, config):
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)
        self._model_config = config.get_text_to_image_config("openai")

    def generate(self, input_data: dict) -> dict:
        """Generate image using DALL-E."""
        prompt = input_data["prompt"]
        size = input_data.get("size", self._model_config.get("size", "1024x1024"))
        quality = input_data.get("quality", self._model_config.get("quality", "standard"))
        model = self._model_config.get("model", "dall-e-3")

        response = self._client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        image_url = response.data[0].url
        relative_path = self._save_image(image_url)
        full_url = UrlHelper.build_output_url(relative_path, self._config)

        return {
            "output_url": full_url,
            "provider": "openai",
            "model": model,
        }

    def get_model_name(self) -> str:
        """Return model name."""
        return self._model_config.get("model", "dall-e-3")

    def _save_image(self, url: str) -> str:
        """Download and save image locally."""
        output_dir = Path(self._config.output_dir) / "images"
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4()}.png"
        filepath = output_dir / filename

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)

        return f"/output/images/{filename}"

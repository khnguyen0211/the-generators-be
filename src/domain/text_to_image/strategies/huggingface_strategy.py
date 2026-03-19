"""Hugging Face Inference API strategy for text-to-image generation."""

import logging
import uuid
import requests
from pathlib import Path

from common.base_strategy import BaseGenerationStrategy
from helpers.url_helper import UrlHelper
from ..prompt_enhancer import PromptEnhancer

logger = logging.getLogger("the_generators")


class HuggingFaceStrategy(BaseGenerationStrategy):
    """Hugging Face Inference API implementation."""

    API_URL = "https://router.huggingface.co/hf-inference/models"

    def __init__(self, config):
        self._config = config
        self._api_key = config.huggingface_api_key
        self._model_config = config.get_text_to_image_config("huggingface")

    def generate(self, input_data: dict) -> dict:
        """Generate image via Hugging Face Inference API."""
        prompt = input_data["prompt"]
        model = self._model_config.get("model", "stabilityai/stable-diffusion-xl-base-1.0")
        category = input_data.get("category")

        is_enhanced = False
        detected_category = None

        if self._config.prompt_enhancer_enabled:
            enhancer = PromptEnhancer(self._config, provider="huggingface")
            result = enhancer.enhance(prompt, category)
            prompt = result["enhanced_prompt"]
            detected_category = result["category"]
            is_enhanced = True

        logger.info(f"[HUGGINGFACE] Calling Inference API | model={model}")

        response = requests.post(
            f"{self.API_URL}/{model}",
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={"inputs": prompt},
            timeout=120,
        )

        if response.status_code != 200:
            error_msg = response.text[:200] if response.text else f"HTTP {response.status_code}"
            logger.error(f"[HUGGINGFACE] API error | status={response.status_code} | {error_msg}")
            raise Exception(f"Hugging Face API error: {error_msg}")

        logger.info(f"[HUGGINGFACE] API response received | size={len(response.content)} bytes")

        relative_path = self._save_image(response.content)
        full_url = UrlHelper.build_output_url(relative_path, self._config)

        logger.info(f"[HUGGINGFACE] Image saved | path={relative_path}")

        return {
            "output_url": full_url,
            "provider": "huggingface",
            "model": model,
            "is_enhanced": is_enhanced,
            "category": detected_category,
        }

    def get_model_name(self) -> str:
        return self._model_config.get("model", "stabilityai/stable-diffusion-xl-base-1.0")

    def _save_image(self, content: bytes) -> str:
        """Save image bytes to output directory."""
        output_dir = Path(self._config.output_dir) / "images"
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4()}.png"
        filepath = output_dir / filename

        with open(filepath, "wb") as f:
            f.write(content)

        return f"/output/images/{filename}"

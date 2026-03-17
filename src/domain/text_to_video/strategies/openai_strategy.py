"""OpenAI Sora strategy for text-to-video generation."""

import logging
import time
import uuid
import requests
from pathlib import Path
from openai import OpenAI

from common.base_strategy import BaseGenerationStrategy
from helpers.url_helper import UrlHelper

logger = logging.getLogger("the_generators")


class OpenAIStrategy(BaseGenerationStrategy):
    """OpenAI Sora implementation."""

    def __init__(self, config):
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)
        self._model_config = config.get_text_to_video_config("openai")

    def generate(self, input_data: dict) -> dict:
        """Generate video using Sora."""
        prompt = input_data["prompt"]
        model = self._model_config.get("model", "sora")

        logger.info(f"[OPENAI] Calling Sora API | model={model}")

        video_job = self._client.videos.create(
            model=model,
            prompt=prompt,
        )

        video_id = self._wait_for_completion(video_job.id)
        logger.info(f"[OPENAI] Video generation completed")

        relative_path = self._save_video(video_id)
        full_url = UrlHelper.build_output_url(relative_path, self._config)

        logger.info(f"[OPENAI] Video saved | path={relative_path}")

        return {
            "output_url": full_url,
            "provider": "openai",
            "model": model,
        }

    def get_model_name(self) -> str:
        """Return model name."""
        return self._model_config.get("model", "sora")

    def _wait_for_completion(self, video_id: str, timeout: int = 600) -> str:
        """Poll until video generation completes. Returns video_id."""
        elapsed = 0
        poll_interval = 5

        while elapsed < timeout:
            job = self._client.videos.retrieve(video_id)
            logger.debug(f"[OPENAI] Video status: {job.status} | progress={getattr(job, 'progress', 'N/A')}%")

            if job.status == "completed":
                return video_id
            if job.status == "failed":
                raise Exception(f"Video generation failed: {getattr(job, 'error', 'Unknown error')}")

            time.sleep(poll_interval)
            elapsed += poll_interval

        raise Exception("Video generation timed out")

    def _save_video(self, video_id: str) -> str:
        """Download and save video locally."""
        output_dir = Path(self._config.output_dir) / "videos"
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4()}.mp4"
        filepath = output_dir / filename

        logger.debug(f"[OPENAI] Downloading video...")
        response = self._client.videos.download_content(video_id=video_id)
        video_bytes = response.read()

        with open(filepath, "wb") as f:
            f.write(video_bytes)

        logger.debug(f"[OPENAI] Video downloaded | size={len(video_bytes)} bytes")

        return f"/output/videos/{filename}"

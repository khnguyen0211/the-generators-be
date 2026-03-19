"""ConfigService - Singleton for environment-based configuration."""

import os
from pathlib import Path
from typing import List, Optional


class ConfigService:
    """Singleton config service. Reads env files based on APP_ENV."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
            cls._instance._environment = ""
        return cls._instance

    def load(self, environment: str = None) -> None:
        """Load config from env file."""
        if environment is None:
            environment = os.environ.get("APP_ENV", "dev")

        self._environment = environment
        base_dir = Path(__file__).resolve().parent.parent.parent
        env_path = base_dir / "env" / f".env.{environment}"
        self._config = self._parse_env_file(env_path)

    def get(self, key: str, default=None):
        """Get config value by key."""
        return self._config.get(key, default)

    def reload(self) -> None:
        """Reload config from current env file."""
        self.load(self._environment)

    @property
    def environment(self) -> str:
        return self._environment

    # ===== API KEYS =====
    @property
    def openai_api_key(self) -> str:
        return self.get("OPENAI_API_KEY", "")

    @property
    def replicate_api_key(self) -> str:
        return self.get("REPLICATE_API_KEY", "")

    @property
    def stability_api_key(self) -> str:
        return self.get("STABILITY_API_KEY", "")

    @property
    def huggingface_api_key(self) -> str:
        return self.get("HUGGINGFACE_API_KEY", "")

    # ===== TEXT TO IMAGE =====
    def get_text_to_image_config(self, provider: str = None) -> dict:
        """Get text-to-image config for specified provider or default."""
        if provider is None:
            provider = self.get("TEXT_TO_IMAGE_DEFAULT", "openai")
        
        prefix = f"TEXT_TO_IMAGE_{provider.upper()}"
        return {
            "provider": provider,
            "model": self.get(f"{prefix}_MODEL", ""),
            "size": self.get(f"{prefix}_SIZE", "1024x1024"),
            "quality": self.get(f"{prefix}_QUALITY", "standard"),
        }

    @property
    def text_to_image_default(self) -> str:
        return self.get("TEXT_TO_IMAGE_DEFAULT", "openai")

    @property
    def text_to_image_models(self) -> List[str]:
        models = self.get("TEXT_TO_IMAGE_MODELS", "openai")
        return [m.strip() for m in models.split(",")]

    # ===== TEXT TO VIDEO =====
    def get_text_to_video_config(self, provider: str = None) -> dict:
        """Get text-to-video config for specified provider or default."""
        if provider is None:
            provider = self.get("TEXT_TO_VIDEO_DEFAULT", "replicate")
        
        prefix = f"TEXT_TO_VIDEO_{provider.upper()}"
        return {
            "provider": provider,
            "model": self.get(f"{prefix}_MODEL", ""),
        }

    @property
    def text_to_video_default(self) -> str:
        return self.get("TEXT_TO_VIDEO_DEFAULT", "replicate")

    @property
    def text_to_video_models(self) -> List[str]:
        models = self.get("TEXT_TO_VIDEO_MODELS", "replicate")
        return [m.strip() for m in models.split(",")]

    # ===== TEXT TO SPEECH =====
    def get_text_to_speech_config(self, provider: str = None) -> dict:
        """Get text-to-speech config for specified provider or default."""
        if provider is None:
            provider = self.get("TEXT_TO_SPEECH_DEFAULT", "openai")
        
        prefix = f"TEXT_TO_SPEECH_{provider.upper()}"
        return {
            "provider": provider,
            "model": self.get(f"{prefix}_MODEL", ""),
            "voice": self.get(f"{prefix}_VOICE", ""),
            "voice_id": self.get(f"{prefix}_VOICE_ID", ""),
        }

    @property
    def text_to_speech_default(self) -> str:
        return self.get("TEXT_TO_SPEECH_DEFAULT", "openai")

    @property
    def text_to_speech_models(self) -> List[str]:
        models = self.get("TEXT_TO_SPEECH_MODELS", "openai")
        return [m.strip() for m in models.split(",")]

    # ===== IMAGE TO VIDEO =====
    def get_image_to_video_config(self, provider: str = None) -> dict:
        """Get image-to-video config for specified provider or default."""
        if provider is None:
            provider = self.get("IMAGE_TO_VIDEO_DEFAULT", "openai")
        
        prefix = f"IMAGE_TO_VIDEO_{provider.upper()}"
        return {
            "provider": provider,
            "model": self.get(f"{prefix}_MODEL", ""),
        }

    @property
    def image_to_video_default(self) -> str:
        return self.get("IMAGE_TO_VIDEO_DEFAULT", "openai")

    @property
    def image_to_video_models(self) -> List[str]:
        models = self.get("IMAGE_TO_VIDEO_MODELS", "openai")
        return [m.strip() for m in models.split(",")]

    # ===== PROMPT ENHANCER =====
    @property
    def prompt_enhancer_enabled(self) -> bool:
        return self.get("PROMPT_ENHANCER_ENABLED", "false").lower() == "true"

    @property
    def prompt_enhancer_openai_model(self) -> str:
        return self.get("PROMPT_ENHANCER_OPENAI_MODEL", "gpt-4")

    @property
    def prompt_enhancer_huggingface_model(self) -> str:
        return self.get("PROMPT_ENHANCER_HUGGINGFACE_MODEL", "Qwen/Qwen2.5-7B-Instruct")

    # ===== SERVER =====
    @property
    def output_dir(self) -> str:
        return self.get("OUTPUT_DIR", "output")

    @property
    def log_dir(self) -> str:
        return self.get("LOG_DIR", "logs")

    @property
    def flask_port(self) -> int:
        return int(self.get("FLASK_PORT", "5000"))

    # ===== DATABASE =====
    @property
    def db_host(self) -> str:
        return self.get("DB_HOST", "localhost")

    @property
    def db_port(self) -> int:
        return int(self.get("DB_PORT", "5432"))

    @property
    def db_name(self) -> str:
        return self.get("DB_NAME", "the_generators")

    @property
    def db_user(self) -> str:
        return self.get("DB_USER", "postgres")

    @property
    def db_password(self) -> str:
        return self.get("DB_PASSWORD", "postgres")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @staticmethod
    def _parse_env_file(path: Path) -> dict:
        """Parse env file: key=value, skip comments and empty lines."""
        config = {}
        if not path.exists():
            return config

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    config[key.strip()] = value.strip()

        return config

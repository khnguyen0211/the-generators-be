"""LoggerService - Daily rotating file logger."""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class LoggerService:
    """Logger with daily file rotation. Dev: file + terminal. Prod: file only."""

    _LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    _DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, config):
        self._config = config
        self._logger = logging.getLogger("the_generators")

    def setup(self) -> None:
        """Initialize logger based on environment."""
        self._logger.handlers.clear()

        log_level = self._config.get("LOG_LEVEL", "INFO").upper()
        self._logger.setLevel(getattr(logging, log_level, logging.INFO))

        formatter = logging.Formatter(self._LOG_FORMAT, datefmt=self._DATE_FORMAT)

        log_dir = self._get_log_dir()
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "app.log")
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        file_handler.suffix = "%Y-%m-%d"
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        if self._config.environment == "dev":
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)

    def info(self, message: str, **kwargs) -> None:
        self._logger.info(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self._logger.error(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self._logger.warning(message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        self._logger.debug(message, **kwargs)

    def _get_log_dir(self) -> str:
        base_dir = Path(__file__).resolve().parent.parent
        log_dir_name = self._config.get("LOG_DIR", "logs")
        return str(base_dir / log_dir_name)

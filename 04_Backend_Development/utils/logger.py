"""
RakshakAI v2
Central Logger
"""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class Logger:
    """
    Central logging utility.
    """

    def __init__(
        self,
        name: str = "RakshakAI",
        log_directory: str = "logs",
        level: int = logging.INFO,
    ):
        self.name = name
        self.log_directory = Path(log_directory)
        self.level = level

        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logger = logging.getLogger(name)

        if not self.logger.handlers:
            self.logger.setLevel(level)

            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

            file_handler = logging.handlers.RotatingFileHandler(
                self.log_directory / "rakshakai.log",
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def exception(
        self,
        message: str,
        exc_info: Optional[bool] = True,
    ):
        self.logger.exception(
            message,
            exc_info=exc_info,
        )

    def get_logger(self):
        return self.logger

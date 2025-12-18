"""Module for configuring logging in the Anime Light application."""
import os
import logging
from typing import Optional

from animelight.settings.settings import Settings

class AnimeLightLogger:
    """
    Anime Light Logger settings
    """
    def __init__(self):
        self.settings = Settings()
        self.log_level = self.settings.LOG_LEVEL
        self.log_file = self.settings.LOGS_DIR / "animelight.log"
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    def get_log_file(self) -> Optional[str]:
        """
        Returns the log file path.
        """
        return self.log_file

    def logger_handlers(self) -> list:
        """
        Returns the logger handlers.
        """
        return [
            logging.FileHandler(self.log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ]

    def setup(self) -> None:
        """
        Configures the logger.
        """
        logging.basicConfig(
            filename=self.log_file,
            level=self.log_level,
            format=self.log_format,
            handlers=self.logger_handlers(),
            filemode="w",
        )


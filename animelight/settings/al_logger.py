"""
Module for configuring logging in the Anime Light application.
"""

import logging
import logging.config
import yaml
from pathlib import Path
from animelight.settings import Settings
from animelight.settings.log_config_file import create_yaml_file

class AnimeLightLogger:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.config_file = self.settings.app_settings.settings_dir / "log_settings.yaml"

        # Crear archivo si no existe
        create_yaml_file(
            log_config_file=self.config_file,
            logs_dir=self.settings.app_settings.logs_dir,
            log_level=self.settings.app_settings.log_level,
            )

        # Cargar configuración
        with open(self.config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)

        # Guardar logger raíz
        self.logger = logging.getLogger("AnimeLight")

    def get_logger(self, name: str = None) -> logging.Logger:
        """
        Devuelve un logger con nombre específico o el central.
        """
        return logging.getLogger(name) if name else self.logger


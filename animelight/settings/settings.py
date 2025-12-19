import os
import yaml
import logging
from pathlib import Path
from typing import Any, Dict

from pydantic import ValidationError
from animelight.models import AppSettings

class Settings:
    APP_DIR = Path.home() / ".animelight"
    CONFIG_FILE = APP_DIR / "config.yaml"
    LOG_CONFIG_FILE = APP_DIR / "log_settings.yaml"
    ENV_FILE = APP_DIR / ".env"

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ensure_dirs()
        self.app_settings = self.load()

    def ensure_dirs(self) -> None:
        """
        Create directories if they don't exist.
        """
        for d in ("temp", "output", "logs", "uploads", "statics"):
            path = self.APP_DIR / d
            path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {path}")

    def load(self) -> AppSettings:
        """
        Load settings from config.yaml and environment variables.
        Priority:
        1. Defaults in AppSettings
        2. config.yaml (if present)
        3. Environment variables / .env
        """
        base: Dict[str, Any] = {}

        # 1) YAML config if exists
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            base = self.merge_yaml(cfg)

        # 2) Construct AppSettings (BaseSettings will merge env/.env automatically)
        try:
            return AppSettings(**base)
        except ValidationError as e:
            self.logger.error(f"Validation error in config file: {e}")
            raise

    def merge_yaml(self, cfg: Dict[str, Any]) -> Dict[str, Any]:
        if not cfg:
            return {}

        app = cfg.get("app", {})
        paths = cfg.get("paths", {})
        merged: Dict[str, Any] = {}

        # App section
        if "api_host" in app: merged["api_host"] = app["api_host"]
        if "api_port" in app: merged["api_port"] = app["api_port"]
        if "log_level" in app: merged["log_level"] = app["log_level"]
        if "api_log_level" in app: merged["api_log_level"] = app["api_log_level"]
        if "allow_credentials" in app: merged["allow_credentials"] = app["allow_credentials"]
        if "allowed_origins" in app: merged["allowed_origins"] = app["allowed_origins"]
        if "allow_methods" in app: merged["allow_methods"] = app["allow_methods"]
        if "allow_headers" in app: merged["allow_headers"] = app["allow_headers"]

        # Paths section
        def expand(p: str) -> Path:
            return Path(os.path.expanduser(p)).resolve()

        for k in ("settings_dir","temp_dir","output_dir","logs_dir","uploads_dir","statics_dir"):
            if k in paths and isinstance(paths[k], str):
                merged[k] = expand(paths[k])

        return merged


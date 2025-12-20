import yaml
from pathlib import Path

def create_yaml_file(log_config_file: Path, logs_dir: Path, log_level: str = "INFO") -> None:
    """
    Write data to a YAML file.

    Args:
        log_config_file (Path): Path to the log configuration file.
        app_dir (Path): Path to the application directory.
        logs_dir (Path): Path to the logs directory.
        log_level (str): Log level.

    Returns:
        None
    """
    # Create log_settings.yaml if not exists
    if not log_config_file.exists():
        log_cfg = {
            "version": 1,
            "formatters": {
                "default": {"format": "%(asctime)s [%(name)s] | %(levelname)s | %(message)s"}
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": str(logs_dir / "animelight.log"),
                    "formatter": "default",
                    "level": log_level,
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "ERROR",
                },
            },
            "root": {
                "handlers": ["file", "console"],
                "level": log_level,
            },
        }
        with open(log_config_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(log_cfg, f, sort_keys=False)
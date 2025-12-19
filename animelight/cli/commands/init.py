"""
Init command to configure YAML configuration for Anime Light application.
"""
import yaml
from pathlib import Path
from rich.table import Table
from argparse import Namespace
from rich.console import Console


from animelight.settings import Settings
from animelight.models import AppSettings

def init_settings(args: Namespace, console: Console) -> None:
    """
    Initialize configuration files and directories.
    """
    app_dir = Settings.APP_DIR
    app_dir.mkdir(parents=True, exist_ok=True)

    # Build AppSettings from CLI args
    app_settings = AppSettings(
        api_host=args.host,
        api_port=int(args.port),
        log_level=args.level,
        settings_dir=app_dir,
        temp_dir=app_dir / "temp",
        output_dir=app_dir / "output",
        logs_dir=app_dir / "logs",
        uploads_dir=app_dir / "uploads",
        statics_dir=app_dir / "statics",
    )

    # Write config.yaml
    config_file = Settings.CONFIG_FILE
    if not config_file.exists():
        config = {
            "app": {
                "api_port": app_settings.api_port,
                "api_host": app_settings.api_host,
                "cli_port": app_settings.cli_port,
                "log_level": app_settings.log_level,
                "api_log_level": app_settings.api_log_level,
                "debug": app_settings.debug,
                "allow_credentials": app_settings.allow_credentials,
                "allowed_origins": app_settings.allowed_origins,
                "allow_methods": app_settings.allow_methods,
                "allow_headers": app_settings.allow_headers,
                "schema_version": app_settings.schema_version
            },
            "paths": {
                "settings_dir": str(app_settings.settings_dir),
                "temp_dir": str(app_settings.temp_dir),
                "output_dir": str(app_settings.output_dir),
                "logs_dir": str(app_settings.logs_dir),
                "uploads_dir": str(app_settings.uploads_dir),
                "statics_dir": str(app_settings.statics_dir),
            },
        }
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(config, f, sort_keys=False)

    # Optional: write .env if requested
    if getattr(args, "env", False):
        env_file = app_dir / ".env"
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(f"API_HOST={app_settings.api_host}\n")
            f.write(f"API_PORT={app_settings.api_port}\n")
            f.write(f"LOG_LEVEL={app_settings.log_level}\n")

    # Create subdirectories
    for d in (app_settings.temp_dir, app_settings.output_dir,
              app_settings.logs_dir, app_settings.uploads_dir,
              app_settings.statics_dir):
        d.mkdir(parents=True, exist_ok=True)

    # Create log_settings.yaml if not exists
    log_config_file = Settings.LOG_CONFIG_FILE
    if not log_config_file.exists():
        log_cfg = {
            "version": 1,
            "formatters": {
                "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": str(app_settings.logs_dir / "animelight.log"),
                    "formatter": "default",
                    "level": app_settings.log_level,
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": app_settings.log_level,
                },
            },
            "root": {
                "handlers": ["file", "console"],
                "level": app_settings.log_level,
            },
        }
        with open(log_config_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(log_cfg, f, sort_keys=False)

    # Show table
    table = Table(title="[bold magenta]Settings Variables[/bold magenta]", border_style="blue", padding=(0, 2))
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Value", style="green")

    table.add_row("API_HOST", app_settings.api_host)
    table.add_row("API_PORT", str(app_settings.api_port))
    table.add_row("LOG_LEVEL", app_settings.log_level)
    table.add_row("ALLOW_CREDENTIALS", str(app_settings.allow_credentials))
    table.add_row("ALLOWED_ORIGINS", str(app_settings.allowed_origins))
    table.add_row("ALLOW_METHODS", str(app_settings.allow_methods))
    table.add_row("ALLOW_HEADERS", str(app_settings.allow_headers))

    table.add_row("APP_DIR", str(app_settings.settings_dir))
    table.add_row("TEMP_DIR", str(app_settings.temp_dir))
    table.add_row("OUTPUT_DIR", str(app_settings.output_dir))
    table.add_row("LOGS_DIR", str(app_settings.logs_dir))
    table.add_row("UPLOADS_DIR", str(app_settings.uploads_dir))
    table.add_row("STATICS_DIR", str(app_settings.statics_dir))

    console.print(table)

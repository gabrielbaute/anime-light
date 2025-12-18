"""
Init command to configure environment variables for SpotifySaver.
"""
from pathlib import Path
from argparse import Namespace
from rich.console import Console
from rich.table import Table

from animelight.settings import Settings
from animelight.models import AppSettings

def init_settings(args: Namespace, console: Console) -> None:
    """
    Loads the initial configuration for the application.
    """

    settings_dir = Settings.SETTINGS_DIR
    settings_dir.mkdir(parents=True, exist_ok=True)

    # Get config values
    app_settings = AppSettings(
        api_host=args.host,
        api_port=int(args.port),
        log_level=args.level,
        settings_dir=settings_dir,
        temp_dir=settings_dir / "temp",
        output_dir=settings_dir / "output",
        logs_dir=settings_dir / "logs",
    )

    env_file = settings_dir / ".env"

    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(f"API_HOST={app_settings.api_host}\n")
            f.write(f"API_PORT={app_settings.api_port}\n")
            f.write(f"LOG_LEVEL={app_settings.log_level}\n")
            f.write(f"SETTINGS_DIR={app_settings.settings_dir}\n")
            f.write(f"TEMP_DIR={app_settings.temp_dir}\n")
            f.write(f"OUTPUT_DIR={app_settings.output_dir}\n")
            f.write(f"LOGS_DIR={app_settings.logs_dir}\n")

    # Creating subdirectories
    app_settings.temp_dir.mkdir(parents=True, exist_ok=True)
    app_settings.output_dir.mkdir(parents=True, exist_ok=True)
    app_settings.logs_dir.mkdir(parents=True, exist_ok=True)
    
    table = Table(title="[bold magenta]Settings Variables[/bold magenta]", border_style="blue", padding=(0, 2))
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Value", style="green")

    table.add_row("API_HOST", app_settings.api_host)
    table.add_row("API_PORT", str(app_settings.api_port))
    table.add_row("LOG_LEVEL", app_settings.log_level)
    table.add_row("SETTINGS_DIR", str(app_settings.settings_dir))
    table.add_row("TEMP_DIR", str(app_settings.temp_dir))
    table.add_row("OUTPUT_DIR", str(app_settings.output_dir))
    table.add_row("LOGS_DIR", str(app_settings.logs_dir))

    console.print(table)

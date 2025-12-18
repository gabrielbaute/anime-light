import os
from pathlib import Path
from argparse import Namespace
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from animelight.settings import Settings
from animelight.models import AppSettings

def show_settings(console: Console) -> None:
    """
    Show actual app settings
    """
    env_file = Settings().SETTINGS_DIR / ".env"

    if not env_file.exists():
        console.print(f"[red]Error:[/red] The {env_file} file does not exist. Please, creates one with the init command")
        return

    load_dotenv(env_file)

    settings_values = AppSettings(
        api_host=os.getenv("API_HOST"),
        api_port=int(os.getenv("API_PORT")),
        log_level=os.getenv("LOG_LEVEL"),
        settings_dir=os.getenv("SETTINGS_DIR"),
        temp_dir=os.getenv("TEMP_DIR"),
        output_dir=os.getenv("OUTPUT_DIR"),
        logs_dir=os.getenv("LOGS_DIR"),
    )

    table = Table(title="[bold magenta]Anime Light Settings[/bold magenta]", border_style="blue", padding=(0, 2))
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Value", style="green")

    table.add_row("API_HOST", settings_values.api_host)
    table.add_row("API_PORT", str(settings_values.api_port))
    table.add_row("LOG_LEVEL", settings_values.log_level)
    table.add_row("SETTINGS_DIR", str(settings_values.settings_dir))
    table.add_row("TEMP_DIR", str(settings_values.temp_dir))
    table.add_row("OUTPUT_DIR", str(settings_values.output_dir))
    table.add_row("LOGS_DIR", str(settings_values.logs_dir))

    console.print(table)
from rich.console import Console
from rich.table import Table

from animelight.settings import Settings

def show_settings(console: Console, settings: Settings) -> None:
    """
    Show actual app settings
    """
    settings_values = settings.app_settings

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
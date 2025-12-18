"""
Clean the app directories
"""
import os
import shutil
from argparse import Namespace
from rich.console import Console
from rich.table import Table

from animelight.settings import Settings
from animelight.cli.utils import count_files_in_directory

def clean_directories(args: Namespace,console: Console) -> None:
    """
    Clean all app directories
    """
    settings = Settings()
    
    if not os.path.exists(settings.SETTINGS_DIR):
        console.print(f"[red]Error:[/red] The {settings.SETTINGS_DIR} directory does not exist")
        return

    if args.all:
        temp_files = count_files_in_directory(settings.TEMP_DIR)
        output_files = count_files_in_directory(settings.OUTPUT_DIR)
        logs_files = count_files_in_directory(settings.LOGS_DIR)

        shutil.rmtree(settings.TEMP_DIR, ignore_errors=True)
        shutil.rmtree(settings.OUTPUT_DIR, ignore_errors=True)
        shutil.rmtree(settings.LOGS_DIR, ignore_errors=True)
        os.remove(settings.SETTINGS_DIR / ".env")

        table = Table(title="[bold magenta]Cleaned Directories[/bold magenta]", border_style="blue", padding=(0, 2))
        table.add_column("Directory", style="cyan", justify="right")
        table.add_column("Files", style="green")
        table.add_row("TEMP_DIR", str(temp_files))
        table.add_row("OUTPUT_DIR", str(output_files))
        table.add_row("LOGS_DIR", str(logs_files))
        console.print(table)
        
    if args.temp:
        temp_files = count_files_in_directory(settings.TEMP_DIR)
        shutil.rmtree(settings.TEMP_DIR, ignore_errors=True)
        console.print(f"[red]{temp_files}[/red] files removed from {settings.TEMP_DIR}")
    
    if args.output:
        output_files = count_files_in_directory(settings.OUTPUT_DIR)
        shutil.rmtree(settings.OUTPUT_DIR, ignore_errors=True)
        console.print(f"[red]{output_files}[/red] files removed from {settings.OUTPUT_DIR}")
    
    if args.logs:
        logs_files = count_files_in_directory(settings.LOGS_DIR)
        shutil.rmtree(settings.LOGS_DIR, ignore_errors=True)
        console.print(f"[red]{logs_files}[/red] files removed from {settings.LOGS_DIR}")
    
    if args.settings:
        os.remove(settings.SETTINGS_DIR / ".env")
        console.print("[red]Settings file removed[/red], please, create one with the init command")
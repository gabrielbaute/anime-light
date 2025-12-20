"""
Clean the app directories
"""
import os
import shutil
from logging import Logger
from argparse import Namespace
from rich.console import Console
from rich.table import Table

from animelight.settings import Settings
from animelight.cli.utils import count_files_in_directory, remove_file

def clean_directories(args: Namespace, console: Console, settings: Settings, logger: Logger = None) -> None:
    """
    Clean all app directories

    Args:
        args (Namespace): the command arguments and flags
        console (Console): Console object from rich
        settings (Settings): Settings object
        logger (Logger): Logger object
    
    Returns:
        None
    """
    
    if not os.path.exists(settings.APP_DIR):
        console.print(f"[red]Error:[/red] The {settings.APP_DIR} directory does not exist")
        return

    if args.all:
        temp_files = count_files_in_directory(settings.app_settings.temp_dir)
        output_files = count_files_in_directory(settings.app_settings.output_dir)
        logs_files = count_files_in_directory(settings.app_settings.logs_dir)
        upload_files = count_files_in_directory(settings.app_settings.uploads_dir)

        logger.info("Cleaning directories")

        shutil.rmtree(settings.app_settings.temp_dir, ignore_errors=True)
        shutil.rmtree(settings.app_settings.output_dir, ignore_errors=True)
        shutil.rmtree(settings.app_settings.logs_dir, ignore_errors=True)
        shutil.rmtree(settings.app_settings.uploads_dir, ignore_errors=True)

        remove_file(settings.APP_DIR, "yaml")
        remove_file(settings.APP_DIR, "env")

        table = Table(title="[bold magenta]Cleaned Directories[/bold magenta]", border_style="blue", padding=(0, 2))
        table.add_column("Directory", style="cyan", justify="right")
        table.add_column("Files", style="green")
        
        table.add_row("TEMP_DIR", str(temp_files))
        table.add_row("OUTPUT_DIR", str(output_files))
        table.add_row("LOGS_DIR", str(logs_files))
        table.add_row("UPLOADS_DIR", str(upload_files))
        console.print(table)
        
    if args.temp:
        temp_files = count_files_in_directory(settings.app_settings.temp_dir)
        logger.info(f"Cleaning temp directory. {temp_files} files removed from {settings.app_settings.temp_dir}")
        shutil.rmtree(settings.app_settings.temp_dir, ignore_errors=True)
        console.print(f"[red]{temp_files}[/red] files removed from {settings.app_settings.temp_dir}")
    
    if args.output:
        output_files = count_files_in_directory(settings.app_settings.output_dir)
        logger.info(f"Cleaning output directory. {output_files} files removed from {settings.app_settings.output_dir}")
        shutil.rmtree(settings.app_settings.output_dir, ignore_errors=True)
        console.print(f"[red]{output_files}[/red] files removed from {settings.app_settings.output_dir}")
    
    if args.logs:
        logs_files = count_files_in_directory(settings.app_settings.logs_dir)
        shutil.rmtree(settings.app_settings.logs_dir, ignore_errors=True)
        console.print(f"[red]{logs_files}[/red] files removed from {settings.app_settings.logs_dir}")
    
    if args.uploads:
        upload_files = count_files_in_directory(settings.app_settings.uploads_dir)
        logger.info(f"Cleaning uploads directory. {upload_files} files removed from {settings.app_settings.uploads_dir}")
        shutil.rmtree(settings.app_settings.uploads_dir, ignore_errors=True)
        console.print(f"[red]{upload_files}[/red] files removed from {settings.app_settings.uploads_dir}")

    if args.settings:
        logger.info("Removing .env file")
        remove_file(settings.APP_DIR, "yaml")
        remove_file(settings.APP_DIR, "env")
        logger.info("Done")
        console.print("[red]Settings file removed[/red], please, create one with the init command")
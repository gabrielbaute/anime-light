"""
Help command for the CLI.
"""
from rich.console import Console
from rich.table import Table

class CommandHelp:
    def __init__(self, console: Console, app_name: str = "al"):
        self.app_name = app_name
        self.console = console
    
    def print_help(self) -> None:
        """
        Shows the general cli help
        """
        table = Table(
            title="[bold magenta]Anime Light CLI Help[/bold magenta]",
            border_style="blue",
            padding=(0, 2),
        )
        table.add_column("Command", style="cyan", justify="right")
        table.add_column("Description", style="green")

        commands = {
            "version": "Show version information",
            "init": "Initialize application settings",
            "settings": "Show actual app settings",
            "help": "Show help information",
            "analyze": "Analyze a video file and show metadata",
            "sysinfo": "Show system information and requirements",
            "convert": "Convert a video file with ffmpeg",
        }

        for cmd, desc in commands.items():
            table.add_row(cmd, desc)

        self.console.print(table)

        self.console.print("\n[bold yellow]Usage examples:[/bold yellow]")
        self.console.print(f"  {self.app_name} version")
        self.console.print(f"  {self.app_name} init --host 127.0.0.1 --port 8000 --level INFO")
        self.console.print(f"  {self.app_name} settings")
        self.console.print(f"  {self.app_name} analyze input.mp4")
        self.console.print(f"  {self.app_name} sysinfo")
        self.console.print(f"  {self.app_name} convert input.mp4 -r 720 -c 23 -p slow -t 4")
        self.console.print(f"  {self.app_name} convert input.mp4 --cool-mode --progress")

    def print_command_help(self, command: str) -> None:
        """
        Shows detailed help for a specific command.

        Args:
            command (str): The command name.

        Returns:
            None
        """
        table = Table(
            title=f"[bold magenta]Help for '{command}' command[/bold magenta]",
            border_style="blue",
            padding=(0, 2),
        )
        table.add_column("Flag / Argument", style="cyan", justify="right")
        table.add_column("Description", style="green")

        if command == "analyze":
            options = {
                "file": "Path to the video file to analyze",
            }
        elif command == "sysinfo":
            options = {}
        elif command == "convert":
            options = {
                "input": "Input video file",
                "output": "Output file (optional, default: ./output/<filename>_converted.mp4)",
                "-r / --resolution": "Video output resolution (360, 480, 720, 1080)",
                "-c / --crf": "Constant Rate Factor (18-28, default: 23)",
                "-p / --preset": "FFmpeg preset (ultrafast, fast, medium, slow, etc.)",
                "-t / --threads": "Number of threads to use",
                "-g / --use-gpu": "Use GPU acceleration if available",
                "--cool-mode": "Force single-thread mode",
                "-b / --batch / --recursive": "Process subfolders or batch mode",
                "--progress": "Show progress bar during conversion",
            }
        elif command == "init":
            options = {
                "--host": "API host (default: 127.0.0.1)",
                "--port": "API port (default: 8000)",
                "--level": "Log level (default: INFO)",
            }
        elif command == "settings":
            options = {}
        elif command == "version":
            options = {}
        elif command == "help":
            options = {
                "command": "Optional command name to show detailed help",
            }

        for opt, desc in options.items():
            table.add_row(opt, desc)

        self.console.print(table)

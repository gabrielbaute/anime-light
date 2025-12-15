from rich.console import Console
from rich.table import Table
from animelight.services import SystemInspectorService

console = Console()

def show_sysinfo() -> None:
    """
    Displays system information and requirements.

    Returns:
        None
    """
    inspector = SystemInspectorService()
    info = inspector.analyze()

    table = Table(title="[bold magenta]System Information[/bold magenta]", border_style="blue")
    table.add_column("Attribute", style="cyan", justify="right")
    table.add_column("Value", style="green")

    table.add_row("OS", f"{info.os_name} {info.os_version}")
    table.add_row("CPU cores", str(info.cpu_cores))
    table.add_row("CPU threads", str(info.cpu_threads))
    table.add_row("FFmpeg available", str(info.ffmpeg_available))
    table.add_row("FFmpeg version", str(info.ffmpeg_version or "-"))

    if info.gpus:
        for gpu in info.gpus:
            table.add_row("GPU", f"{gpu.name} (Driver {gpu.driver_version})")
    else:
        table.add_row("GPU", "Not detected")

    console.print(table)

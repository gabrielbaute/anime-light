"""
Analyze command for video files.
"""
from pathlib import Path
from rich.console import Console
from rich.table import Table

from animelight.services import VideoAnalyzerService
from animelight.cli.utils import convert_bytes_to_mb


def analyze_video(file: Path, console: Console) -> None:
    """
    Analyze a video file and display its metadata.

    Args:
        file (Path): Path to the video file.

    Returns:
        None
    """
    service = VideoAnalyzerService(file)
    info = service.analyze()

    if not info:
        console.print(f"[red]Error:[/red] The file could not be analyzed {file}")
        return
    size = convert_bytes_to_mb(info.size_bytes)

    table = Table(title=f"[bold magenta]Video Analysis[/bold magenta]: {file.name}", border_style="blue")
    table.add_column("Atributo", style="cyan", justify="right")
    table.add_column("Valor", style="green")

    table.add_row("Path", str(info.path))
    table.add_row("Size", str(f"{size:.2f} MB"))
    table.add_row("Formats", ", ".join(info.formats))
    table.add_row("Format long name", str(info.format_long_name or "-"))
    table.add_row("Duration (s)", f"{info.duration_seconds:.2f}")
    table.add_row("Resolution", f"{info.width}x{info.height}")
    table.add_row("FPS", str(info.fps))
    table.add_row("Video codec", info.video_codec)
    table.add_row("Audio codec", str(info.audio_codec or "-"))
    table.add_row("Bitrate video", str(info.bitrate_video or "-"))
    table.add_row("Bitrate audio", str(info.bitrate_audio or "-"))
    table.add_row("Streams", str(info.streams))

    console.print(table)
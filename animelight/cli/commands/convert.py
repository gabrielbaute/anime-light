"""
Convert command for video files.
"""
from pathlib import Path
from logging import Logger
from rich.console import Console
from rich.table import Table
from argparse import Namespace

from animelight.enums import (
    FfmpegPresets,
    VideoResolution,
    GPUMethods,
    AudioBitrates,
    VideoCodecs,
    AudioCodecs,
)
from animelight.models import ConversionResult
from animelight.settings import Settings
from animelight.services import VideoAnalyzerService, VideoConverterService

def run_convert(args: Namespace, console: Console, settings: Settings, logger: Logger = None) -> None:
    """
    Execute the conversion of a video file.

    Args:
        args (Namespace): the command arguments and flags
        console (Console): Console object from rich
        settings (Settings): Settings object
        logger (Logger): Logger object
        
    Returns:
        None
    """
    resolution_map = {
        360: VideoResolution.P_360,
        480: VideoResolution.P_480,
        720: VideoResolution.P_720,
        1080: VideoResolution.P_1080,
    }
    
    scale = resolution_map.get(args.resolution, VideoResolution.P_720)
    preset = FfmpegPresets(args.preset) if args.preset else FfmpegPresets.MEDIUM
    
    gpu_method = None
    if args.use_gpu:
        # TODO: lógica más avanzada con sysinfo
        gpu_method = GPUMethods.NVIDIA  # por defecto

    # Threads
    threads = 1 if args.cool_mode else (args.threads or 1)
    try:
        logger.info("Starting Analysis")
        input_path = Path(args.input)
        analyzer = VideoAnalyzerService(input_path, logger=logger)
        video_info = analyzer.analyze()
        if not video_info:
            logger.error(f"Failed at analyzing file: {input_path}")
            console.print(f"[red]Error:[/red] Failed at analyzing file: {input_path}")
            return

        output_dir = Path(args.output).parent if args.output else settings.app_settings.output_dir
        service = VideoConverterService(video_info, output_dir=output_dir, settings=settings, logger=logger)

        logger.info("Starting Conversion")
        result: ConversionResult = service.convert_with_progress_bar(
            crf=args.crf or 23,
            preset=preset,
            scale=scale,
            console=console,
            gpu_method=gpu_method,
            audio_bitrate=AudioBitrates.B_128K,
            video_codec=VideoCodecs.H264,
            audio_codec=AudioCodecs.AAC,
            threads=threads,
        )

        table = Table(title="[bold magenta]Conversion Result[/bold magenta]", border_style="blue")
        table.add_column("Attribute", style="cyan", justify="right")
        table.add_column("Value", style="green")

        table.add_row("ID", result.id)
        table.add_row("Success", str(result.success))
        table.add_row("Input", str(result.input_file))
        table.add_row("Output", str(result.output_file or "-"))
        table.add_row("Command", " ".join(result.command))
        table.add_row("Duration (s)", str(result.duration_seconds or "-"))
        table.add_row("Error", str(result.error_message or "-"))

        console.print(table)
    except KeyboardInterrupt: 
        logger.warning("Conversion cancelled by user (Ctrl+C)") 
        console.print("[yellow]Conversion cancelled by user.[/yellow]")
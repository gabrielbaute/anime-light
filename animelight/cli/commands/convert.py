"""
Convert command for video files.
"""
from pathlib import Path
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
from animelight.services.video_analyzer_service import VideoAnalyzerService
from animelight.services.video_converter_service import VideoConverterService

def run_convert(args: Namespace, console: Console) -> None:
    """
    Ejecuta la conversión de video usando los parámetros de argparse.
    """
    # Mapear resolución (int -> Enum)
    resolution_map = {
        360: VideoResolution.P_360,
        480: VideoResolution.P_480,
        720: VideoResolution.P_720,
        1080: VideoResolution.P_1080,
    }
    scale = resolution_map.get(args.resolution, VideoResolution.P_720)

    # Mapear preset
    preset = FfmpegPresets(args.preset) if args.preset else FfmpegPresets.MEDIUM

    # GPU
    gpu_method = None
    if args.use_gpu:
        # TODO: lógica más avanzada con sysinfo
        gpu_method = GPUMethods.NVIDIA  # por defecto

    # Threads
    threads = 1 if args.cool_mode else (args.threads or 1)

    # Analizar el video primero para obtener VideoFileInfo
    input_path = Path(args.input)
    analyzer = VideoAnalyzerService(input_path)
    video_info = analyzer.analyze()
    if not video_info:
        console.print(f"[red]Error:[/red] No se pudo analizar el archivo {input_path}")
        return

    # Determinar directorio de salida
    if args.output:
        output_dir = Path(args.output).parent
    else:
        output_dir = Path("output")

    # Crear servicio de conversión
    service = VideoConverterService(video_info, output_dir=output_dir)

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

    # Mostrar resultado con rich
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

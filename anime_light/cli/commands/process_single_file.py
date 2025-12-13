
import os
import fnmatch
from pathlib import Path
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from anime_light.cli.utils import select_converter

def process_single_file(input_path: str, output_dir: str, resolution: str, crf: int, preset: str, progress) -> bool:
    """Procesa un único archivo con barra de progreso."""
    try:
        converter_class = select_converter(resolution)
        converter = converter_class(input_path, output_dir=output_dir)
        
        task = progress.add_task(
            f"Convirtiendo {os.path.basename(input_path)}...",
            filename=os.path.basename(input_path),
            total=100
        )
        
        def update_progress(percent: int):
            progress.update(task, completed=percent)
        
        return converter.convert(
            crf=crf,
            preset=preset,
            progress_callback=update_progress
        )
    except ValueError as e:
        progress.console.print(f"[red]❌ {e}")
        return False
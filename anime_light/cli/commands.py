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
        
        def update_progress(percent):
            progress.update(task, completed=percent)
        
        return converter.convert(
            crf=crf,
            preset=preset,
            progress_callback=update_progress
        )
    except ValueError as e:
        progress.console.print(f"[red]❌ {e}")
        return False

def process_batch(input_dir: str, output_dir: str, resolution: str, crf: int, preset: str, 
                 recursive: bool = False, exclude_patterns: list = None):
    """Procesa archivos válidos en una carpeta (opcionalmente en subcarpetas)."""
    supported_formats = (".mp4", ".mkv", ".avi")
    exclude_patterns = exclude_patterns or []
    converted_files = 0

    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        transient=True
    ) as progress:
        try:
            converter_class = select_converter(resolution)
        except ValueError as e:
            progress.console.print(f"[red]❌ {e}")
            return

        for root, _, files in os.walk(input_dir) if recursive else [(input_dir, [], os.listdir(input_dir))]:
            rel_path = os.path.relpath(root, input_dir)
            
            for filename in files:
                if (filename.lower().endswith(supported_formats) and 
                    not any(fnmatch.fnmatch(filename, pattern) for pattern in exclude_patterns)):
                    
                    input_path = os.path.join(root, filename)
                    output_subdir = os.path.join(output_dir, rel_path) if recursive else output_dir
                    Path(output_subdir).mkdir(parents=True, exist_ok=True)
                    
                    task = progress.add_task(
                        f"Convirtiendo {filename}...",
                        filename=filename,
                        total=100
                    )
                    
                    def update_progress(percent):
                        progress.update(task, completed=percent)
                    
                    converter = converter_class(input_path, output_dir=output_subdir)
                    if converter.convert(crf=crf, preset=preset, progress_callback=update_progress):
                        converted_files += 1

        if converted_files > 0:
            progress.console.print(f"[green]✓ {converted_files} archivos convertidos en: {output_dir}")
        else:
            progress.console.print("[yellow]⚠️ No se encontraron archivos compatibles")


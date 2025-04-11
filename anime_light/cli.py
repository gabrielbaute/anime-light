import subprocess
import sys
import os
import argparse
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from anime_light.core.converter import Convert480p, Convert720p

console = Console()

def check_ffmpeg():
    """Verifica si FFmpeg está instalado."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        console.print("[red]❌ FFmpeg no está instalado o no está en el PATH.")
        return False

def process_single_file(input_path: str, output_dir: str, resolution: str, crf: int, preset: str, progress) -> bool:
    """Procesa un único archivo con barra de progreso."""
    converter_class = Convert480p if resolution == "480p" else Convert720p
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

def process_batch(input_dir: str, output_dir: str, resolution: str, crf: int, preset: str):
    """Procesa todos los archivos válidos de una carpeta."""
    supported_formats = (".mp4", ".mkv", ".avi")
    converted_files = 0
    
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        TextColumn("•"),
        TextColumn("[bold green]{task.fields[filename]}"),
        transient=True  # Oculta la barra al completarse
    ) as progress:
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(input_dir, filename)
                if process_single_file(input_path, output_dir, resolution, crf, preset, progress):
                    converted_files += 1
        
        if converted_files > 0:
            progress.console.print(f"[green]✓ {converted_files} archivos convertidos en: {output_dir}")
        else:
            progress.console.print("[yellow]⚠️ No se encontraron archivos compatibles en la carpeta")

def main():
    if not check_ffmpeg():
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Convierte videos de anime a resoluciones ligeras.")
    parser.add_argument("input", help="Ruta del archivo o carpeta")
    parser.add_argument("-r", "--resolution", choices=["480p", "720p"], default="480p")
    parser.add_argument("--crf", type=int, default=23, help="Calidad (18-28, menor=mejor)")
    parser.add_argument("--preset", default="slow", choices=["fast", "slow", "veryslow"])
    parser.add_argument("--output-dir", default=None, help="Directorio base de salida (las subcarpetas 480p/720p se crearán aquí)")
    
    args = parser.parse_args()

    # Configurar directorios de salida
    output_base_dir = args.output_dir if args.output_dir else os.path.join(
        os.path.dirname(args.input) if os.path.isfile(args.input) else args.input,
        "output"
    )
    output_dir = os.path.join(output_base_dir, args.resolution)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if os.path.isfile(args.input):
        # Modo archivo único
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TextColumn("•"),
            TextColumn("[bold green]{task.fields[filename]}"),
        ) as progress:
            if process_single_file(args.input, output_dir, args.resolution, args.crf, args.preset, progress):
                console.print(f"[green]✓ Conversión completada! Guardado en: {output_dir}")
    
    elif os.path.isdir(args.input):
        # Modo batch
        process_batch(args.input, output_dir, args.resolution, args.crf, args.preset)
    
    else:
        console.print("[red]❌ La ruta no es un archivo ni una carpeta válida.")

if __name__ == "__main__":
    main()
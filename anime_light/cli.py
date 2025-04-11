import subprocess, sys, os, argparse
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from anime_light.core.converter import Convert480p, Convert720p

console = Console()

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        console.print("[red]❌ FFmpeg no está instalado o no está en el PATH.")
        return False

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

    # Determinar el directorio base para output
    if args.output_dir:
        output_base_dir = args.output_dir
    else:
        # Si es un archivo, usamos su directorio padre. Si es carpeta, usamos la carpeta misma.
        base_path = os.path.dirname(args.input) if os.path.isfile(args.input) else args.input
        output_base_dir = os.path.join(base_path, "output")
    
    # Crear directorio de salida (resolución específica)
    output_dir = os.path.join(output_base_dir, args.resolution)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Configurar barra de progreso
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        TextColumn("•"),
        TextColumn("[bold green]{task.fields[filename]}"),
    ) as progress:
        task = progress.add_task(f"Convirtiendo a {args.resolution}...", filename=os.path.basename(args.input), total=100)
        
        def update_progress(percent):
            progress.update(task, completed=percent)
        
        if os.path.isfile(args.input):
            # Conversión para un solo archivo
            converter = Convert480p(args.input, output_dir=output_dir) if args.resolution == "480p" else Convert720p(args.input, output_dir=output_dir)
            success = converter.convert(
                crf=args.crf,
                preset=args.preset,
                progress_callback=update_progress
            )
            if success:
                console.print(f"[green]✓ Conversión completada! Guardado en: {output_dir}")
        elif os.path.isdir(args.input):
            # Procesamiento por lotes (opcional: implementar aquí)
            console.print("[yellow]⚠️ Procesamiento por lotes aún no implementado")

if __name__ == "__main__":
    main()
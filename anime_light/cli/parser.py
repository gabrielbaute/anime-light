import argparse

def create_parser():
    """Configura los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="Anime-light",
        
        usage="Convierte archivos de video a mp4 ligero mediante ffmpeg.",
        description="Convierte videos de anime a resoluciones ligeras.",
        epilog="Ejemplo: anime-light input.mkv -r 720p --crf 23 --preset slow --output-dir ./output",
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True,)
    
    parser.add_argument("-v", "--version", action="store_true", help="Mostrar versión y salir")
    
    subparsers = parser.add_subparsers(dest="command", required=False, help="Comandos disponibles")

    # -------------------------------------------
    # Subcomando: convert
    # -------------------------------------------
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convertir un archivo de anime"
    )
    
    convert_parser.add_argument("input", help="Ruta del archivo o carpeta")
    convert_parser.add_argument("-r", "--resolution", choices=["360p", "480p", "720p", "1080p"], default="480p")
    convert_parser.add_argument("--crf", type=int, default=23, help="Calidad (18-28, menor=mejor)")
    convert_parser.add_argument("--preset", default="slow", choices=["ultrafast", "superfast", "fast", "slow", "veryslow"])
    convert_parser.add_argument("--output-dir", default=None, help="Directorio base de salida")
    convert_parser.add_argument("--recursive", action="store_true", help="Procesar subcarpetas")
    convert_parser.add_argument("--exclude", nargs="+", default=[], help="Patrones para excluir archivos")
    convert_parser.add_argument("--threads", type=int, default=1, help="Número de hilos CPU a usar (1-2, etc)")
    convert_parser.add_argument("--cool-mode", action="store_true", help="Prioriza reducir temperatura (usa preset fast y 1 hilo)")
    convert_parser.add_argument("--use-gpu", type=str, choices=["qsv", "cuda", "vaapi", "d3d12va"], default=None, help="Usar aceleración por GPU (opciones: qsv para Intel, cuda para NVIDIA, etc.)")
    
    return parser
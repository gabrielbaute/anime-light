# anime_light/core/utils.py
import subprocess
from rich.console import Console

console = Console()

def check_ffmpeg() -> bool:
    """Verifica si FFmpeg está instalado."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        console.print("[red]❌ FFmpeg no está instalado o no está en el PATH.")
        return False

def select_converter(resolution: str):
    """Selecciona la clase de conversión."""
    from anime_light.core.converter import Convert360p, Convert480p, Convert720p, Convert1080p  # Import local para evitar circularidad
    converters = {
        "360p": Convert360p,
        "480p": Convert480p,
        "720p": Convert720p,
        "1080p": Convert1080p
    }
    if resolution not in converters:
        raise ValueError(f"Resolución no soportada: {resolution}")
    return converters[resolution]
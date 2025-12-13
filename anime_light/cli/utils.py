# Funciones de utilidad variadas
import subprocess
from typing import List, Optional
from rich.console import Console

from anime_light.core import Convert360p, Convert480p, Convert720p, Convert1080p
from anime_light.core.converter import VideoConverter


console = Console()

def check_ffmpeg() -> bool:
    """Verifica si FFmpeg está instalado."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        console.print("[red]❌ FFmpeg no está instalado o no está en el PATH.")
        return False

def select_converter(resolution: str) -> VideoConverter:
    """
    Selecciona la clase de conversión.
    
    Args:
        resolution (str): Resolución deseada ("360p", "480p", "720p", "1080p").
    
    Returns:
        VideoConverter: Clase de conversión seleccionada.
    
    Raises:
        ValueError: Si la resolución no es válida.
    """
    converters = {
        "360p": Convert360p,
        "480p": Convert480p,
        "720p": Convert720p,
        "1080p": Convert1080p
    }
    if resolution not in converters:
        raise ValueError(f"Resolución no soportada: {resolution}")
    return converters[resolution]

def validate_gpu_acceleration(method: str) -> bool:
    """Versión optimizada usando get_available_hwaccels()."""
    return method.lower() in get_available_hwaccels()

def get_available_hwaccels() -> List[str]:
    """Obtiene métodos de aceleración disponibles, ignorando la primera línea (header)."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-hwaccels"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Filtra líneas y excluye el header "Hardware acceleration methods:"
        return [
            line.strip() for line in result.stdout.splitlines()[1:] 
            if line.strip() and not line.startswith("Hardware")
        ]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
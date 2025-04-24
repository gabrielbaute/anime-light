# Funciones de utilidad variadas
import subprocess
from rich.console import Console
from rich.table import Table

console = Console()
__version__ = "0.3.1"

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

def validate_gpu_acceleration(method: str) -> bool:
    """Versión optimizada usando get_available_hwaccels()."""
    return method.lower() in get_available_hwaccels()

def get_available_hwaccels() -> list:
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

def show_version():
    """Muestra la versión en una tabla estilo Rich."""
    console = Console()
    table = Table(
        title="[bold magenta]anime-light[/bold magenta]",
        show_header=False,
        border_style="blue",
        padding=(0, 2),
    )
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Value", style="green")
    
    table.add_row("[yellow]Build[/yellow]", "[bold]stable[/bold]")
    table.add_row("Versión", f"[bold]{__version__}[/bold]")
    table.add_row("Autor", "Gabriel Baute")
    table.add_row("Licencia", "MIT")
    table.add_row("Repo", "https://github.com/gabrielbaute/anime-light")

    console.print(table)
import os
import re
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from rich.progress import Progress
from rich.console import Console
import subprocess
from typing import Optional

class VideoConverter(ABC):
    """Clase base abstracta para conversiones de video con FFmpeg."""
    
    def __init__(self, input_path: str, output_dir: str = "output", temp_dir: str = "temp"):
        """
        Args:
            input_path (str): Ruta del video de entrada.
            output_dir (str): Carpeta para archivos finales.
            temp_dir (str): Carpeta para archivos temporales.
        """
        self.input_path = input_path
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.console = Console()
        
        Path(self.output_dir).mkdir(exist_ok=True)
        Path(self.temp_dir).mkdir(exist_ok=True)
        
        self.input_filename = os.path.basename(input_path)
        self.output_filename = self._generate_output_filename()
        self.temp_path = os.path.join(self.temp_dir, self.output_filename)
        self.output_path = os.path.join(self.output_dir, self.output_filename)


    def _build_gpu_params(self, gpu_method: str) -> list:
        """Genera parámetros específicos para cada método de GPU."""
        gpu_params = []
        
        if gpu_method == "qsv":  # Intel
            gpu_params.extend([
                "-hwaccel", "qsv",
                "-hwaccel_output_format", "qsv",
                "-c:v", "h264_qsv",
                "-global_quality", str(self.crf),  # Mapea CRF a calidad en QSV
                "-preset", "fast"
            ])
        elif gpu_method == "cuda":  # NVIDIA
            gpu_params.extend([
                "-hwaccel", "cuda",
                "-hwaccel_output_format", "cuda",
                "-c:v", "h264_nvenc",
                "-cq", str(self.crf),  # NVENC usa -cq (similar a CRF)
                "-preset", "p4"        # p1 (más rápido) a p7 (mejor compresión)
            ])
        elif gpu_method == "vaapi":  # AMD/Linux
            gpu_params.extend([
                "-hwaccel", "vaapi",
                "-hwaccel_output_format", "vaapi",
                "-c:v", "h264_vaapi",
                "-qp", str(self.crf),  # VAAPI usa -qp
                "-quality", "speed"
            ])
        
        return gpu_params

    @abstractmethod
    def _generate_output_filename(self) -> str:
        """Genera el nombre del archivo de salida (ej: 'video[480p].mp4')."""
        pass

    @abstractmethod
    def _get_ffmpeg_scale(self) -> str:
        """Devuelve el filtro de escala de FFmpeg (ej: 'scale=640:480')."""
        pass

    @staticmethod
    def convert_batch(
        input_dir: str,
        output_dir: str,
        resolution: str = "480p",
        crf: int = 23,
        preset: str = "slow"
    ) -> None:
        """
        Convierte todos los videos de una carpeta.
        
        Args:
            input_dir (str): Carpeta con videos de entrada.
            output_dir (str): Carpeta de salida.
            resolution (str): "480p" o "720p".
            crf (int): Calidad del video.
            preset (str): Preset de FFmpeg.
        """
        converter_class = Convert480p if resolution == "480p" else Convert720p
        for filename in os.listdir(input_dir):
            if filename.endswith((".mp4", ".mkv")):
                input_path = os.path.join(input_dir, filename)
                converter = converter_class(input_path, output_dir=output_dir)
                converter.convert(crf=crf, preset=preset)

    def convert(
        self,
        crf: int = 23,
        preset: str = "slow",
        gpu_method: Optional[str] = None,
        threads: int = 1,
        audio_bitrate: str = "128k",
        progress_callback=None,
        remove_temp: bool = True
    ) -> bool:
        """
        Método principal para la conversión.
        
        Args:
            crf (int): Calidad del video (18-28).
            preset (str): Velocidad de compresión (slow, fast, etc.).
            audio_bitrate (str): Bitrate de audio (ej: "64k").
            remove_temp (bool): Eliminar archivo temporal al finalizar.
            
        Returns:
            bool: True si la conversión fue exitosa.
        """
        cmd = ["ffmpeg"]

        if gpu_method:
            cmd.extend(self._build_gpu_params(gpu_method))
            # Escalado específico para GPU
            if gpu_method == "qsv":
                cmd.extend(["-vf", f"scale_qsv={self._get_ffmpeg_scale().replace('scale=', '')}"])
            elif gpu_method == "cuda":
                cmd.extend(["-vf", f"scale_cuda={self._get_ffmpeg_scale().replace('scale=', '')}"])
        else:
            cmd.extend([
                "-i", self.input_path,
                "-threads", str(threads),
                "-vf", self._get_ffmpeg_scale(),
                "-c:v", "libx264",
                "-crf", str(crf),
                "-preset", preset
            ])
        
        # 2. Añade parámetros comunes (audio, overwrite)
        cmd.extend([
            "-tune", "animation",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", audio_bitrate,
            "-y",
            self.temp_path
        ])
        
        try:
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)
            duration, time_pattern = None, re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")
            
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                if duration is None and "Duration:" in line:
                    duration_match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", line)
                    if duration_match:
                        duration = sum(float(x) * 60 ** i for i, x in enumerate(reversed(duration_match.groups())))
                time_match = time_pattern.search(line)
                if time_match and duration:
                    current_time = sum(float(x) * 60 ** i for i, x in enumerate(reversed(time_match.groups())))
                    percent = (current_time / duration) * 100
                    if progress_callback:  # Notificar al CLI
                        progress_callback(percent)

            if process.wait() == 0:
                shutil.move(self.temp_path, self.output_path)
                #self.console.print(f"\n[green]✅ Conversión exitosa: {self.output_path}")
                return True
            else:
                self.console.print("\n[red]❌ Error en la conversión\n")
                return False

        except FileNotFoundError:
            self.console.print("[red]❌ FFmpeg no está instalado o no está en el PATH.")
            return False
        finally:
            if remove_temp and os.path.exists(self.temp_path):
                os.remove(self.temp_path)

    def set_output_filename(self, new_name: str):
        """Personaliza el nombre del archivo de salida."""
        self.output_filename = new_name
        self.temp_path = os.path.join(self.temp_dir, self.output_filename)
        self.output_path = os.path.join(self.output_dir, self.output_filename)

class Convert360p(VideoConverter):
    """Conversor específico para resolución 360p (640x360)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[360p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=640:360:flags=lanczos"  # Relación de aspecto 16:9


class Convert480p(VideoConverter):
    """Conversor específico para resolución 480p (640x480)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[480p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=640:480:flags=lanczos"  # Relación 4:3 (común en anime antiguo)


class Convert720p(VideoConverter):
    """Conversor específico para resolución 720p (1280x720)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[720p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=1280:720:flags=lanczos"  # 16:9 HD

class Convert1080p(VideoConverter):
    """Conversor específico para resolución 1080p (1920x1080)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[1080p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=1920:1080:flags=lanczos"  # 16:9 Full HD
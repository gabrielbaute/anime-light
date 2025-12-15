import os
from typing import Optional
from animelight.core.converter import VideoConverter
from animelight.core.convert_480 import Convert480p
from animelight.core.convert_720 import Convert720p

class ConvertBatch(VideoConverter):
    """Clase para manejar conversiones por lotes de videos a múltiples resoluciones."""
    
    def __init__(self, input_path: str, output_dir: str, temp_dir: str):
        self.input_path = input_path
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.converters = [
            Convert480p(input_path, output_dir, temp_dir),
            Convert720p(input_path, output_dir, temp_dir)
        ]
    
    def convert_all(self, progress_callback: Optional[callable] = None) -> bool:
        """Convierte el video a todas las resoluciones especificadas."""
        total_converters = len(self.converters)
        
        for index, converter in enumerate(self.converters):
            success = converter.convert_video(
                progress_callback=lambda percent: progress_callback(
                    (index + percent / 100) / total_converters * 100
                ) if progress_callback else None
            )
            if not success:
                return False
        
        return True

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
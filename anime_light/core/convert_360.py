import os
from anime_light.core.converter import VideoConverter

class Convert360p(VideoConverter):
    """Conversor específico para resolución 360p (640x360)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[360p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=640:360:flags=lanczos"  # Relación de aspecto 16:9
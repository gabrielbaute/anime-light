import os
from animelight.core.converter import VideoConverter

class Convert480p(VideoConverter):
    """Conversor específico para resolución 480p (640x480)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[480p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=640:480:flags=lanczos"  # Relación 4:3 (común en anime antiguo)
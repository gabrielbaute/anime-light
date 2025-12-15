import os
from animelight.core.converter import VideoConverter

class Convert1080p(VideoConverter):
    """Conversor específico para resolución 1080p (1920x1080)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[1080p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=1920:1080:flags=lanczos"  # 16:9 Full HD
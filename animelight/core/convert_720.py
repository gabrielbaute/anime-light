import os
from animelight.core.converter import VideoConverter

class Convert720p(VideoConverter):
    """Conversor específico para resolución 720p (1280x720)."""
    
    def _generate_output_filename(self) -> str:
        return f"{os.path.splitext(self.input_filename)[0]}[720p].mp4"

    def _get_ffmpeg_scale(self) -> str:
        return "scale=1280:720:flags=lanczos"  # 16:9 HD

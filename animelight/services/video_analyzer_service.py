import subprocess
import json
from logging import Logger
from pathlib import Path
from typing import List, Dict, Optional
from animelight.models.video_file import VideoFileInfo

class VideoAnalyzerService:
    """
    Analyzes a video file and returns its information.
    """
    def __init__(self, file_path: Path, logger: Logger = None):
        self.file_path = file_path
        self.logger = logger
        self.data = self.get_raw_info()

    def get_raw_info(self) -> dict:
        """
        Returns the raw information of the video file.

        Returns:
            dict: Raw information of the video file.
        """
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size,format_name,format_long_name:stream=codec_type,codec_name,width,height,r_frame_rate,bit_rate",
            "-of", "json",
            str(self.file_path)
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            self.logger.debug(f"Raw info: {data}")
            return data
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running ffprobe: {e}")
            return {}

    def get_raw_format_info(self) -> Dict:
        """
        Returns the raw format information of the video file.

        Returns:
            Dict: Raw format information of the video file.
        """
        return self.data["format"]

    def get_formats(self) -> List[str]:
        """
        Returns the formats of the video file.

        Returns:
            List[str]: Formats of the video file.
        """
        format_info = self.get_raw_format_info()
        format_name = format_info.get("format_name", "")
        self.logger.debug(f"Getting formats: {format_name}")
        return format_name.split(",") if format_name else []

    
    def get_video_stream(self) -> Dict:
        """
        Returns the video stream of the video file.

        Returns:
            Dict: Video stream of the video file.
        """
        self.logger.debug(f"Getting video stream.")
        return next((s for s in self.data["streams"] if s.get("codec_type") == "video"), None)
    
    def get_audio_stream(self) -> Dict:
        """
        Returns the audio stream of the video file.

        Returns:
            Dict: Audio stream of the video file.
        """
        self.logger.debug(f"Getting audio stream.")
        return next((s for s in self.data["streams"] if s.get("codec_type") == "audio"), None)

    def analyze(self) -> Optional[VideoFileInfo]:
        """
        Analyzes the video file and returns a VideoFileInfo object.

        Returns:
            VideoFileInfo: Video file information.
        """
        if not self.data:
            self.logger.error(f"Could not retrieve raw info for {self.file_path}")
            return None
        
        self.logger.debug(f"Analyzing video file: {self.file_path}")
        format_info = self.get_raw_format_info()
        format_long_name = format_info.get("format_long_name", None)
        video_stream = self.get_video_stream()
        audio_stream = self.get_audio_stream()
        streams = self.data.get("streams", [])

        return VideoFileInfo(
            path=self.file_path,
            size_bytes=int(format_info["size"]),
            formats=self.get_formats(),
            format_long_name=format_long_name if format_long_name else None,
            duration_seconds=float(format_info["duration"]),
            width=int(video_stream["width"]),
            height=int(video_stream["height"]),
            fps=eval(video_stream["r_frame_rate"]),  # ej. "30000/1001"
            video_codec=video_stream["codec_name"],
            audio_codec=audio_stream["codec_name"] if audio_stream else None,
            bitrate_video=int(video_stream.get("bit_rate", 0)) if video_stream else None,
            bitrate_audio=int(audio_stream.get("bit_rate", 0)) if audio_stream else None,
            streams=len(streams)
        )
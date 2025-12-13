from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List

class VideoFileInfo(BaseModel):
    """
    Keywords:
        path (Path): Path to the video file.
        size_bytes (int): Size of the video file in bytes.
        formats (List[str]): Formats of the video file that ffmpeg recognizes.
        format_long_name (Optional[str]): Long name of the video format.
        duration_seconds (float): Duration of the video in seconds.
        width (int): Width of the video.
        height (int): Height of the video.
        fps (float): Frames per second of the video.
        video_codec (str): Video codec used in the video.
        audio_codec (Optional[str]): Audio codec used in the video.
        bitrate_video (Optional[int]): Bitrate of the video in bits per second.
        bitrate_audio (Optional[int]): Bitrate of the audio in bits per second.
        streams (int): Number of streams in the video.
    """
    path: Path
    size_bytes: int
    formats: List[str]
    format_long_name: Optional[str] = None
    duration_seconds: float
    width: int
    height: int
    fps: float
    video_codec: str
    audio_codec: Optional[str] = None
    bitrate_video: Optional[int] = None
    bitrate_audio: Optional[int] = None
    streams: int

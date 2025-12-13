from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List


class ConversionResult(BaseModel):
    """
    Keywords:
        success (bool): Whether the conversion was successful.
        input_file (Path): Path to the input video file.
        output_file (Optional[Path]): Path to the output video file.
        command (List[str]): FFmpeg command that was used to convert the video.
        log (Optional[str]): Log of the conversion.
        duration_seconds (Optional[float]): Duration of the video in seconds.
        error_message (Optional[str]): Error message if the conversion failed.
    """
    success: bool
    input_file: Path
    output_file: Optional[Path] = None
    command: List[str]
    log: Optional[str] = None
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
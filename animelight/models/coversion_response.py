from pydantic import BaseModel
from typing import List, Optional
from animelight.models.video_file import VideoFileInfo
from animelight.models.conversion_result import ConversionResult

class ConversionResponse(BaseModel):
    """
    Response for a video conversion request.

    Keywords:
        success (bool): Whether the conversion was successful.
        filename (Optional[str]): Name of the converted video file.
        video_input_info (Optional[VideoFileInfo]): Information about the input video file.
        video_output_info (Optional[VideoFileInfo]): Information about the output video file.
        convert_result (Optional[ConversionResult]): Result of the video conversion.
        download_url (Optional[str]): URL to download the converted video file.
        error_message (Optional[str]): Error message if the conversion failed.
        efficiency (Optional[float]): Efficiency of the video conversion.
    """
    success: bool
    filename: Optional[str] = None
    video_input_info: Optional[VideoFileInfo] = None
    video_output_info: Optional[VideoFileInfo] = None
    convert_result: Optional[ConversionResult] = None
    download_url: Optional[str] = None
    error_message: Optional[str] = None
    efficiency: Optional[float] = None


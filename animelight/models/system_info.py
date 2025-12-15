from pydantic import BaseModel
from typing import List, Optional

from animelight.models.gpu_info import GPUInfo

class SystemInfo(BaseModel):
    """
    SystemInfo contains information about the system.

    Keywords:
        os_name (str): Name of the operating system.
        os_version (str): Version of the operating system.
        cpu_cores (int): Number of CPU cores.
        cpu_threads (int): Number of CPU threads.
        gpus (Optional[List[GPUInfo]]): List of GPU information.
        ffmpeg_available (bool): Whether ffmpeg is available.
        ffmpeg_version (Optional[str]): Version of ffmpeg.
    """
    os_name: str
    os_version: str
    cpu_cores: int
    cpu_threads: int
    gpus: Optional[List[GPUInfo]] = None
    ffmpeg_available: bool
    ffmpeg_version: Optional[str] = None

from pydantic import BaseModel
from typing import List, Optional

from anime_light.models.gpu_info import GPUInfo

class SystemInfo(BaseModel):
    os_name: str
    os_version: str
    cpu_cores: int
    cpu_threads: int
    gpus: Optional[List[GPUInfo]] = None
    ffmpeg_available: bool
    ffmpeg_version: Optional[str] = None

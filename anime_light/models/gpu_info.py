from pydantic import BaseModel
from typing import Optional

class GPUInfo(BaseModel):
    """
    GPUInfo contains information about a GPU.

    Keywords:
        name (str): Name of the GPU.
        driver_version (Optional[str]): Driver version of the GPU.
    """
    name: str
    driver_version: Optional[str] = None
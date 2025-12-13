from pydantic import BaseModel
from typing import Optional

class GPUInfo(BaseModel):
    name: str
    driver_version: Optional[str] = None
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List


class ConversionResult(BaseModel):
    success: bool
    input_file: Path
    output_file: Optional[Path] = None
    command: List[str]
    log: Optional[str] = None
    duration_seconds: Optional[float] = None
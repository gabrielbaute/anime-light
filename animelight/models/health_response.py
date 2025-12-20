from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthcheckResponse(BaseModel):
    name: str
    version: str
    status: str
    timestamp: datetime
    message: Optional[str] = None
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthcheckResponse(BaseModel):
    """
    Response for a healthcheck request.

    Keywords:
        name (str): Name of the service.
        version (str): Version of the service.
        status (str): Status of the service.
        timestamp (datetime): Timestamp of the healthcheck.
        error_message (Optional[str]): Error message if the healthcheck failed.
    """
    name: str
    version: str
    status: str
    timestamp: datetime
    message: Optional[str] = None
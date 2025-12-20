from pydantic import BaseModel
from typing import List, Optional

class CleanResponse(BaseModel):
    """
    Response for a clean request.

    Keywords:
        success (bool): Whether the clean was successful.
        message (str): Message about the clean.
        files_removed (List[str]): List of files removed.
        error_message (Optional[str]): Error message if the clean failed.
    """
    success: bool
    message: str
    files_removed: List[str]
    error_message: Optional[str] = None
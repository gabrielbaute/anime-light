from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health"])

__version__ = "0.4.0"

@router.get("", summary="Healthcheck endpoint")
def healthcheck():
    return {
        "name": "AnimeLight",
        "version": f"{__version__}",
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
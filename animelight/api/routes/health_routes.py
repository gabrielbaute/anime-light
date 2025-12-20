from fastapi import APIRouter
from datetime import datetime
from animelight.models import HealthcheckResponse

router = APIRouter(prefix="/health", tags=["Health"])

__version__ = "0.4.0"

@router.get("", summary="Healthcheck endpoint", response_model=HealthcheckResponse)
def healthcheck():
    healthcheck_response = HealthcheckResponse(
        name="AnimeLight",
        version=f"{__version__}",
        status="ok",
        timestamp=datetime.now()
    )
    return healthcheck_response
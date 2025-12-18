from fastapi import APIRouter
from animelight.services import SystemInspectorService
from animelight.models import SystemInfo, GPUInfo

router = APIRouter(prefix="/sysinfo", tags=["System Info"])

@router.get("", summary="Get system information", response_model=SystemInfo)
def get_system_info():
    system = SystemInspectorService()
    return system.analyze()
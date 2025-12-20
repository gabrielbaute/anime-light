from animelight.api.routes.health_routes import router as health_router
from animelight.api.routes.sys_info_route import router as sys_info_router
from animelight.api.routes.convert_routes import router as convert_router
from animelight.api.routes.clean_routes import router as clean_router

__all__ = ["health_router", "sys_info_router", "convert_router", "clean_router"]
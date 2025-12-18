from fastapi import FastAPI
from animelight.api.routes import health_router, sys_info_router

def include_routers(app: FastAPI):
    """
    Include routers for API routes
    """
    app.include_router(health_router)
    app.include_router(sys_info_router)
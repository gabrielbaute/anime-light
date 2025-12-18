from fastapi import FastAPI
from animelight.api.routes import health_router, sys_info_router

def include_routers(app: FastAPI, prefix: str):
    """
    Include routers for API routes
    """
    app.include_router(health_router, prefix=prefix, tags=["Health"])
    app.include_router(sys_info_router, prefix=prefix, tags=["System Info"])
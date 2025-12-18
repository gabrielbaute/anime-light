from fastapi import FastAPI
from animelight.api.routes import health_router, sys_info_router

def include_routers(app: FastAPI, prefix: str) -> None:
    """
    Include routers for API routes

    Args:
        app (FastAPI): FastAPI application instance
        prefix (str): Prefix for API routes
    
    Returns:
        None
    """
    app.include_router(health_router, prefix=prefix, tags=["Health"])
    app.include_router(sys_info_router, prefix=prefix, tags=["System Info"])
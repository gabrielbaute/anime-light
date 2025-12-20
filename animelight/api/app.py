"""
FastAPI Application Factory
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from animelight.settings import Settings
from animelight.api.include_routers import include_routers

__version__ = "0.4.0"

def create_app(settings: Settings) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="AnimeLight API",
        description="Convert video files to lightweight mp4 using ffmpeg.",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app_settings.allowed_origins,
        allow_credentials=settings.app_settings.allow_credentials,
        allow_methods=settings.app_settings.allow_methods,
        allow_headers=settings.app_settings.allow_headers,
    )

    include_routers(app, prefix="/api/v1")

    return app
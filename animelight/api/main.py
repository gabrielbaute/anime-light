import uvicorn

from animelight.settings import Settings, AnimeLightLogger
from animelight.api.app import create_app

settings = Settings()

logger_factory = AnimeLightLogger(settings=settings)
logger = logger_factory.get_logger()

app = create_app(settings=settings)
app.state.logger = logger

def run_server():
    """
    Run the FastAPI server.
    """
    uvicorn.run(
        "animelight.api.main:app",
        host=settings.app_settings.api_host,
        port=settings.app_settings.api_port,
        log_level=settings.app_settings.api_log_level,
        reload=True,
    )

if __name__ == "__main__":
    run_server()
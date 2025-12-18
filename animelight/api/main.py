import uvicorn

from animelight.settings import Settings
from animelight.api.app import create_app

app = create_app()

def run_server(settings: Settings):
    """
    Run the FastAPI server.
    """
    uvicorn.run(
        "animelight.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=True,
    )

if __name__ == "__main__":
    settings = Settings()
    settings.load_settings()
    print(settings.API_PORT)
    run_server(settings)
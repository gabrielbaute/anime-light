"""
Application Settings model
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """
    Settings value for the application.

    Keywords:
        # Server
        api_port (int): Port for the API server.
        api_host (str): Host for the API server.
        cli_port (int): Port for the CLI server.
        log_level (str): Log level for the application.
        api_log_level (str): Log level for the API server.
        debug (bool): Debug mode for the application.
        allow_credentials (bool): Allow credentials for CORS.
        allowed_origins (list[str]): List of allowed origins for CORS.
        allow_methods (list[str]): List of allowed methods for CORS.
        allow_headers (list[str]): List of allowed headers for CORS.
        schema_version: int = 1

        # Directories
        settings_dir (Path): Directory for settings files.
        temp_dir (Path): Directory for temporary files.
        output_dir (Path): Directory for output files.
        logs_dir (Path): Directory for log files.
        uploads_dir (Path): Directory for uploaded files.
        statics_dir (Path): Directory for static files.
    """
    api_port: int = 8000
    api_host: str = "127.0.0.1"
    cli_port: int = 9000
    log_level: str = "INFO"
    api_log_level: str = "info"
    debug: bool = False
    allow_credentials: bool = True
    allowed_origins: list[str] = ["*"]
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]
    schema_version: int = 1

    settings_dir: Path = Path.home() / ".animelight"
    temp_dir: Path = Path.home() / ".animelight" / "temp"
    output_dir: Path = Path.home() / ".animelight" / "output"
    logs_dir: Path = Path.home() / ".animelight" / "logs"
    uploads_dir: Path = Path.home() / ".animelight" / "uploads"
    statics_dir: Path = Path.home() / ".animelight" / "statics"
    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
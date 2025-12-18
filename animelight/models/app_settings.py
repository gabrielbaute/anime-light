from pathlib import Path
from pydantic import BaseModel

class AppSettings(BaseModel):
    """
    Settings value for the application.

    Keywords:
        api_port (int): Port for the API server.
        api_host (str): Host for the API server.
        log_level (str): Log level for the application.
        settings_dir (Path): Directory for settings files.
        temp_dir (Path): Directory for temporary files.
        output_dir (Path): Directory for output files.
        logs_dir (Path): Directory for log files.
    """
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    log_level: str = "info"
    settings_dir: Path = Path.home() / ".animelight"
    temp_dir: Path = Path.home() / ".animelight" / "temp"
    output_dir: Path = Path.home() / ".animelight" / "output"
    logs_dir: Path = Path.home() / ".animelight" / "logs"
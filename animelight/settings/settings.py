import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.load_settings()

    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info").lower()
    
    # App directories
    SETTINGS_DIR = Path.home() / ".animelight"
    TEMP_DIR = Path.home() / ".animelight" / "temp"
    OUTPUT_DIR = Path.home() / ".animelight" / "output"
    LOGS_DIR = Path.home() / ".animelight" / "logs"


    def load_settings(self):
        """Load settings from ~/.animelight/.env file with fallback."""
        # Primary: Load from ~/.animelight/.env (created by init command)
        env_file = self.SETTINGS_DIR / ".env"

        if env_file.exists():
            load_dotenv(env_file)
        else:
            # Fallback: Load from project root .env (backward compatibility)
            env_path = Path(__file__).resolve().parents[2] / ".env"
            load_dotenv(env_path)
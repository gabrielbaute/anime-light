import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List

class Settings:
    def __init__(self):
        pass

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
            print(f"Loading settings from {env_file}")
            load_dotenv(env_file)
        else:
            # Fallback: Load from project root .env (backward compatibility)
            print(f"Loading settings from project root .env")
            env_path = Path(__file__).resolve().parents[2] / ".env"
            load_dotenv(env_path)

    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    API_ALLOWED_ORIGINS: List[str] = ["*"]
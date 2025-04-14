import os

BASE_DIR=os.path.abspath(os.path.dirname(__file__))

class Config:
    """General configuration class."""

    UPLOAD_FOLDER = os.path.join(BASE_DIR, '../temp')
    APP_NAME = "Anime Light"
    APP_VERSION = "0.3.1"
    PORT = 5001
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    APP_REPOSITORY = "https://github.com/gabrielbaute/anime-light"
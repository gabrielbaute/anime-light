import shutil
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request

from animelight.settings import Settings

router = APIRouter(prefix="/clean", tags=["Maintenance"])
settings = Settings()

@router.delete("", summary="Clean temp, uploads and output directories")
async def clean_directories(request: Request):
    logger = getattr(request.app.state, "logger", None)

    try:
        dirs_to_clean = [
            settings.app_settings.temp_dir,
            settings.app_settings.uploads_dir,
            settings.app_settings.output_dir,
        ]

        cleaned = []
        for d in dirs_to_clean:
            if d.exists() and d.is_dir():
                for item in d.iterdir():
                    try:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                        cleaned.append(str(item))
                    except Exception as e:
                        if logger:
                            logger.error(f"Failed to delete {item}: {e}")
        if logger:
            logger.info(f"Cleaned directories: {cleaned}")

        return {
            "success": True,
            "message": "Directories cleaned successfully",
            "files_removed": cleaned,
        }
    except Exception as e:
        if logger:
            logger.error(f"Error cleaning directories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

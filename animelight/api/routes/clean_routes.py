import shutil
from pathlib import Path
from typing import Literal
from fastapi import APIRouter, HTTPException, Request, Query

from animelight.settings import Settings

router = APIRouter(prefix="/clean", tags=["Maintenance"])
settings = Settings()

@router.delete("", summary="Clean specific directories")
async def clean_directories(
    request: Request,
    target: Literal["uploads", "temp", "output", "all"] = Query("all", description="Directory to clean")
):
    logger = getattr(request.app.state, "logger", None)

    try:
        dirs_map = {
            "uploads": settings.app_settings.uploads_dir,
            "temp": settings.app_settings.temp_dir,
            "output": settings.app_settings.output_dir,
        }

        # Seleccionar directorios
        if target == "all":
            dirs_to_clean = dirs_map.values()
        else:
            dirs_to_clean = [dirs_map[target]]

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
            logger.info(f"Cleaned {target} directories: {cleaned}")

        return {
            "success": True,
            "message": f"{target.capitalize()} directories cleaned successfully",
            "files_removed": cleaned,
        }
    except Exception as e:
        if logger:
            logger.error(f"Error cleaning directories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

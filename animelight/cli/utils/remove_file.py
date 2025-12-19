from pathlib import Path

def remove_file(path: Path, ext: str) -> bool:
    """
    Remove the file with the given extension
    """
    file = path / f"*.{ext}"
    if file.exists():
        file.unlink()
        return True
            
    return False
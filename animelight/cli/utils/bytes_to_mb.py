
def convert_bytes_to_mb(bytes: int) -> float:
    """
    Convert bytes to megabytes.

    Args:
        bytes (int): Number of bytes.

    Returns:
        float: Number of megabytes.
    """
    return bytes / (1024 * 1024)
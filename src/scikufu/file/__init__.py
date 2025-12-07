import os


def exists(file_path: os.PathLike) -> bool:
    """
    Checks if a file exists at the given path.

    Args:
        file_path (os.PathLike): The path to the file.
    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

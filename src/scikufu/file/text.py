import os
from pathlib import Path


def read(file_path: os.PathLike, encoding: str = "utf-8") -> str:
    """
    Reads the content of a text file and returns it as a string.

    Args:
        file_path (os.PathLike): The path to the text file.
    Returns:
        str: The content of the text file.
    """
    with open(file_path, "r", encoding=encoding) as file:
        content = file.read()
    return content


def write(file_path: os.PathLike, content: str, encoding: str = "utf-8") -> None:
    """
    Writes a string to a text file.

    Args:
        file_path (os.PathLike): The path to the text file.
        content (str): The content to write to the file.
        encoding (str): The encoding to use when writing the file. Defaults to "utf-8".
    """
    write_path = Path(file_path)
    write_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding=encoding) as file:
        file.write(content)


def append(file_path: os.PathLike, content: str, encoding: str = "utf-8") -> None:
    """
    Appends a string to a text file.

    Args:
        file_path (os.PathLike): The path to the text file.
        content (str): The content to append to the file.
        encoding (str): The encoding to use when writing the file. Defaults to "utf-8".
    """
    with open(file_path, "a", encoding=encoding) as file:
        file.write(content)

import os
import json

from pathlib import Path
from typing import List, Dict, Any, Union, Generator


def read(
    file_path: os.PathLike, encoding: str = "utf-8"
) -> Generator[Dict[str, Any], None, None]:
    """
    Reads the content of a JSON Lines file and returns it as a generator of dictionaries.

    Args:
        file_path (os.PathLike): The path to the JSON Lines file.
        encoding (str): The encoding to use when reading the file. Defaults to "utf-8".
    Returns:
        Generator[Dict[str, Any], None, None]: A generator that yields dictionaries from the file.
    """
    with open(file_path, "r", encoding=encoding) as file:
        for line in file:
            line = line.strip()
            if line:
                yield json.loads(line)


def write(
    file_path: os.PathLike, data: List[Dict[str, Any]], encoding: str = "utf-8"
) -> None:
    """
    Writes a list of dictionaries to a JSON Lines file.

    Args:
        file_path (os.PathLike): The path to the JSON Lines file.
        data (list): A list of dictionaries to write to the file.
        encoding (str): The encoding to use when writing the file. Defaults to "utf-8".
    """
    write_path = Path(file_path)
    write_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding=encoding) as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")


def append(
    file_path: os.PathLike,
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    encoding: str = "utf-8",
) -> None:
    """
    Appends a list of dictionaries to a JSON Lines file.

    Args:
        file_path (os.PathLike): The path to the JSON Lines file.
        data (list): A list of dictionaries to append to the file.
        encoding (str): The encoding to use when writing the file. Defaults to "utf-8".
    """
    if isinstance(data, dict):
        data = [data]  # Convert single dict to list for consistency
    with open(file_path, "a", encoding=encoding) as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")

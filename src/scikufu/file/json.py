import scikufu.file.text

import json
import os

from pathlib import Path


def read(file_path: os.PathLike, encoding: str = "utf-8") -> dict:
    """
    Reads the content of a JSON file and returns it as a dictionary.

    Args:
        file_path (os.PathLike): The path to the JSON file.
        encoding (str): The encoding to use when reading the file. Defaults to "utf-8".
    Returns:
        dict: The content of the JSON file as a dictionary.
    """
    content = scikufu.file.text.read(file_path, encoding)
    return json.loads(content)


def write(
    file_path: os.PathLike, data: dict, encoding: str = "utf-8", indent: int = 4
) -> None:
    """
    Writes a dictionary to a JSON file.

    Args:
        file_path (os.PathLike): The path to the JSON file.
        data (dict): The dictionary to write to the file.
        encoding (str): The encoding to use when writing the file. Defaults to "utf-8".
        indent (int): The number of spaces to use for indentation in the JSON file. Defaults to 4.
    """
    write_path = Path(file_path)
    write_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, ensure_ascii=False, indent=indent)
    scikufu.file.text.write(file_path, content, encoding)


def append(
    file_path: os.PathLike, data: dict, encoding: str = "utf-8", indent: int = 4
) -> None:
    """
    Appends a dictionary to a JSON file.

    Args:
        file_path (os.PathLike): The path to the JSON file.
        data (dict): The dictionary to append to the file.
        encoding (str): The encoding to use when writing the file. Defaults to "utf-8".
        indent (int): The number of spaces to use for indentation in the JSON file. Defaults to 4.
    """
    existing_data = read(file_path, encoding)
    existing_data.update(data)
    write(file_path, existing_data, encoding, indent)

from typing import Union
from pathlib import Path

PathIsh = Union[str, Path]


def expand_path(path: PathIsh) -> Path:
    if isinstance(path, str):
        path = Path(path)
    return path.expanduser().absolute()

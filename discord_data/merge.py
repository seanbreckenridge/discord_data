import warnings
import logging
from pathlib import Path
from typing import Set, Optional, Iterator, List, Sequence

from .model import Json, Message, Activity
from .common import PathIsh, expand_path
from .parse import (
    parse_messages,
    parse_raw_activity,
    _parse_activity_blob,
)


# handles resolving the paths from the top-level export_dir
# or a list of paths
def _list_exports(
    search_for_folder: str,  # messages or activity
    export_dir: Optional[PathIsh] = None,
    paths: Optional[Sequence[PathIsh]] = None,
) -> List[Path]:
    exports: List[Path] = []
    if paths is not None:
        for p in map(expand_path, paths):
            if not p.name == search_for_folder:
                warnings.warn(f"Expected {p} to end with {search_for_folder}...")
            exports.append(p)
    else:
        if export_dir is None:
            raise RuntimeError(
                "Did not supply an 'export_dir' (top-level dir with multiple exports) or 'paths' (the activity/messages dirs themselves"
            )
        for p in expand_path(export_dir).iterdir():
            # sanity-check, to make sure this is the right path
            fdir = p / search_for_folder
            if fdir.exists():
                exports.append(fdir)
            else:
                warnings.warn(
                    f"Directory not found: Expected {search_for_folder} directory at {fdir}"
                )
    return exports


def merge_raw_activity(
    *,
    export_dir: Optional[PathIsh] = None,
    paths: Optional[Sequence[PathIsh]] = None,
    logger: Optional[logging.Logger] = None,
) -> Iterator[Json]:
    emitted: Set[str] = set()
    for p in _list_exports("activity", export_dir, paths):
        for blob in parse_raw_activity(p, logger=logger):
            key: str = blob["event_id"]
            if key in emitted:
                continue
            yield blob
            emitted.add(key)


def merge_activity(
    *,
    export_dir: Optional[PathIsh] = None,
    paths: Optional[Sequence[PathIsh]] = None,
    logger: Optional[logging.Logger] = None,
) -> Iterator[Activity]:
    yield from map(
        _parse_activity_blob,
        merge_raw_activity(export_dir=export_dir, paths=paths, logger=logger),
    )


def merge_messages(
    *,
    export_dir: Optional[PathIsh] = None,
    paths: Optional[Sequence[PathIsh]] = None,
) -> Iterator[Message]:
    emitted: Set[int] = set()
    for p in _list_exports("messages", export_dir, paths):
        for msg in parse_messages(p):
            key: int = msg.message_id
            if key in emitted:
                continue
            yield msg
            emitted.add(msg.message_id)

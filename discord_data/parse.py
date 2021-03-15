import json
import csv
import logging

from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional, Dict, List, Any


from .model import Message, Channel, Json
from .common import expand_path, PathIsh


def _get_self_user_id(export_root_dir: PathIsh) -> str:
    user_info_f: Path = expand_path(export_root_dir) / "account" / "user.json"
    assert user_info_f.exists()
    user_json = json.loads(user_info_f.read_text())
    return str(user_json["id"])


def _parse_datetime(ds: str) -> datetime:
    try:
        return datetime.strptime(ds, r"%Y-%m-%d %H:%M:%S.%f%z")
    except ValueError:
        return datetime.strptime(ds, r"%Y-%m-%d %H:%M:%S%z")


def parse_messages(messages_dir: PathIsh) -> Iterator[Message]:
    pmsg_dir: Path = expand_path(messages_dir)
    # get user id
    my_user: str = _get_self_user_id(pmsg_dir.parent)

    # parse index
    index_f = pmsg_dir / "index.json"
    assert index_f.exists(), f"Message index 'index.json' doesnt exist at {index_f}"
    index: Dict[str, Optional[str]] = json.loads(index_f.read_text())

    # get individual message directories
    msg_dirs: List[Path] = list(
        filter(lambda d: d.is_dir() and not d.name.startswith("."), pmsg_dir.iterdir())
    )
    for msg_chan in msg_dirs:

        channel_json: Dict[str, Any] = json.loads(
            (msg_chan / "channel.json").read_text()
        )
        server_name: Optional[str] = None
        if "guild" in channel_json:
            server_name = channel_json["guild"]["name"]
        channel_name: Optional[str] = index.get(channel_json["id"])

        channel_obj: Channel = Channel(
            cid=channel_json["id"], name=channel_name, server_name=server_name
        )

        # read CSV file to get messages
        with (msg_chan / "messages.csv").open("r", encoding="utf-8", newline="") as f:
            csv_reader = csv.reader(
                f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            next(csv_reader)  # ignore header row
            for row in csv_reader:
                yield Message(
                    mid=row[0],
                    dt=_parse_datetime(row[1]),
                    channel=channel_obj,
                    content=row[2],
                    attachments=row[3],
                )


def parse_activity(
    events_dir: Path, logger: Optional[logging.Logger] = None
) -> Iterator[Json]:
    for activity_f in expand_path(events_dir).rglob("*.json"):
        if logger is not None:
            logger.debug(f"Parsing {activity_f}...")
        # not a 'json file', this has json objects, one per line
        for line in activity_f.open("r"):
            yield json.loads(line)
